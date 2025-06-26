# 🌍 Travel Trend AI Generator

**An automated Azure Function that uses Google Trends, Azure OpenAI, and SendGrid to generate and email SEO-optimized travel blog content weekly, based on trending travel keywords.**

---

## ✈️ Overview

This project automates travel content creation by:
- Pulling real-time trending keywords from Google Trends (via PyTrends)
- Using Azure OpenAI to generate a full SEO blog post
- Sending the content to your inbox weekly with SendGrid

It's a hands-off way to keep your travel blog or newsletter fresh with content that's timely and relevant.

---

## 🧰 Tech Stack

| Tool            | Purpose                                |
|-----------------|----------------------------------------|
| **Azure Functions** | Scheduled execution (weekly timer) |
| **PyTrends**     | Pull trending Google search terms     |
| **Azure OpenAI** | Generate blog content using GPT       |
| **SendGrid**     | Email the generated post              |
| **Python 3.11**  | Main language/runtime used            |

---

## 🗂️ File Structure

travel-trend-ai-generator/
   - init.py # Main function logic
   - function.json # Azure Function trigger config
   - requirements.txt # Python dependencies
   - funcignore # Exclude local files from deployment

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/RichGerg/travel-trend-ai-generator.git

2. **Install dependencies**
   pip install -r requirements.txt

3. **Configure environment variables**
   Set these as Application Settings in your Azure Function:
   - AZURE_OPENAI_KEY
   - AZURE_OPENAI_ENDPOINT
   - AZURE_OPENAI_DEPLOYMENT
   - SENDGRID_API_KEY

4. **Deploy to Azure**
   func azure functionapp publish <your-function-app-name> --python

5. **Example Output**
   The script sends a blog post like this:
   Title: 5 Affordable Beach Destinations to Book Right Now!
   Intro: Looking for travel deals? Here are 5 trending getaways you don't want to miss...
   ...

![Mock Form](https://www.phishy.cloud/assets/img/proj/img-form-1.jpg)

---

💡 **Use Cases**
   - Automating SEO content for travel websites
   - Weekly newsletters
   - Blog inspiration based on real search trends
   - AI content workflows for digital marketing

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

## ✉️ Credits

Created by RichGerg - built as an automated lightweight tool that uses Google Trends, Azure OpenAI, and SendGrid to generate and email SEO-optimized travel blog content weekly, based on trending travel keywords.
