import random
import logging
import os
import datetime
import azure.functions as func
from pytrends.request import TrendReq
from openai import AzureOpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# STEP 1: Determine the most relevant trending keyword based on the current month
def get_trending_keyword():
    month = datetime.datetime.now().strftime("%B")
    pytrends = TrendReq(hl='en-US', tz=360)

    # Monthly seasonal seed keywords
    monthly_seed_map = {
        "January": ["winter getaways", "ski trips", "warm destinations", "new year travel"],
        "February": ["romantic escapes", "valentine's day trips", "weekend getaways"],
        # ...rest of months...
        "December": ["christmas vacations", "new year getaways", "winter wonderlands"]
    }

    # Event-specific seed keywords
    event_map = {
        "January": ["CES Las Vegas", "Sundance Film Festival"],
        "March": ["Spring Break", "SXSW Austin"],
        # ...rest of events...
        "December": ["Christmas markets Europe", "New Year's Eve destinations"]
    }

    # Try pulling rising search queries from Google Trends
    for seed_group, source in [
        (event_map.get(month, []), "event seed"),
        (monthly_seed_map.get(month, []), "monthly seed")
    ]:
        for seed in seed_group:
            try:
                pytrends.build_payload([seed], geo='US', timeframe='now 7-d')
                rising = pytrends.related_queries().get(seed, {}).get("rising")
                if rising is not None and not rising.empty:
                    keyword = rising.iloc[0]["query"]
                    logging.info(f"Found trending keyword from {source}: {keyword}")
                    return keyword
            except Exception as e:
                logging.error(f"Error checking seed '{seed}' from {source}: {e}")

    # Fallback keyword selection if no trend data found
    fallback_map = {
        "January": ["winter getaways", "ski trips"],
        "February": ["valentine's day ideas", "weekend getaways"],
        # ...rest of months...
        "December": ["winter holidays", "new year escapes"]
    }

    fallback_keywords = fallback_map.get(month, ["travel deals", "cheap flights", "bucket list destinations"])
    choice = random.choice(fallback_keywords)
    logging.warning(f"No trending data found — using seasonal fallback: {choice}")
    return choice

# STEP 2: Generate a long-form SEO blog post using Azure OpenAI
def generate_seo_blog(keyword, deployment, api_key, endpoint):
    try:
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-03-01-preview",
            azure_endpoint=endpoint
        )

        prompt = f"""
        Write a detailed blog post targeting the keyword: "{keyword}".
        - Title: Include something about "travel deals" or "cheap flights"
        - Introduction: 1 short paragraph introducing the topic and teasing 5 destinations
        - Body: Write 5 destination sections. Each section should be a natural, well-written paragraph of at least 5 sentences. Seamlessly include reasons why it's a great destination, cost-saving tips, and what makes it uniquely appealing—without using bullet points or mini-headings.
        - CTA: End with a call to action to search Jetsetz.com for the best travel deals before they're gone.
        - Tone: Friendly, helpful, enthusiastic, slight sense of urgency
        """

        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=1200
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating blog content: {e}"

# STEP 3: Send generated content via SendGrid email
def send_email_via_sendgrid(subject, content):
    try:
        message = Mail(
            from_email='from@email.com',  # Replace if needed
            to_emails='to@email.com',  # ⚠️ Replace before pushing public
            subject=subject,
            html_content=content.replace('\n', '<br>')  # Convert line breaks to HTML
        )
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        logging.info(f"Email sent: {response.status_code}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# STEP 4: Azure Function Timer Trigger Entry Point (runs weekly)
def main(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("⏰ The timer is past due!")

    keyword = get_trending_keyword()

    blog_post = generate_seo_blog(
        keyword,
        deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    send_email_via_sendgrid(
        subject=f"Weekly Travel Blog: {keyword.title()}",
        content=blog_post
    )

    logging.info("\n📝 Final Blog Post Content:\n%s", blog_post)
