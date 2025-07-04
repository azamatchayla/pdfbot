_# PDF Bot

This is a Telegram bot that generates a PDF file from images sent by users. It accepts images, stores them temporarily, and compiles them into a single PDF file upon user request.

## Features
✅ Accepts JPG and PNG images  
✅ Generates a multi-page PDF  
✅ Shows an ad before sending PDF  
✅ Automatically cleans up temporary files  

## Requirements
- python-telegram-bot==20.3  
- fpdf  
- pillow  
- aiohttp==3.8.4  

## Usage
1️⃣ Start the bot using `/start`.  
2️⃣ Send your images (JPG, PNG).  
3️⃣ Press the "📄 PDF yaratish" button.  
4️⃣ The bot will display an ad, generate the PDF, and send it to you after 30 seconds.  

## Deployment

You can deploy this bot on platforms like Render.

### Environment Variables
Set the following environment variable:

### Example Procfile
web: python main.py

### Example requirements.txt
python-telegram-bot==20.3
fpdf
pillow
aiohttp==3.8.4
### Example .gitignore
*.jpg
*.png
*.pdf
__pycache__/
temp/
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support
If you have any questions or issues, feel free to open an issue on GitHub or contact the author.

## License
MIT
