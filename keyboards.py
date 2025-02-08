from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Function to generate semester selection buttons
def semester_menu(category):
    keyboard = [
        [InlineKeyboardButton(f" Semester {i}", callback_data=f"{category}_semester_{i}")] for i in range(1, 9)
    ]
    return InlineKeyboardMarkup(keyboard)

# Function to generate a back button
def back_button():
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="go_back")]]
    return InlineKeyboardMarkup(keyboard)
