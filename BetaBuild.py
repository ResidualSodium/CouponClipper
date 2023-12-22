############~~~~~~~ Import Libraries ~~~~~~~############
import os
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time
import sys
from tkinter import *
import tkinter as tk
import customtkinter

############~~~~~~~ Global variables for pathing ~~~~~~~############
user = os.getlogin()

############~~~~~~~ Lists && random settings needed ~~~~~~~############

possible_profile_names = ["default", "Default"]
possible_directories = ["C:\\", "D:\\", "E:\\", "F:\\"]

# list of departments to be used in v1.1 or v1.2
list_of_departments = ['Adult Beverage', 'Baby', 'Bakery', 'Baking Goods', 'Beauty', 'Beverages', 'Breakfast',
                       'Candy', 'Canned & Packaged', 'Cleaning Products', 'Condiment & Sauces', 'Dairy', 'Deli',
                       'Electronics', 'Frozen', 'Garden & Patio', 'General', 'Gift Cards', 'Hardware', 'Health',
                       'Health & Beauty', 'Home Decor', 'Kitchen', 'Meat & Seafood', 'Natural & Organic', 'Other',
                       'Pasta Sauces Grain', 'Personal Care', 'Pet Care', 'Produce', 'Snacks', 'Tobacco']

food_for_less_list_of_departments = ['Adult Beverage', 'Baby', 'Bakery', 'Baking Goods', 'Beauty', 'Beverages',
                                     'Breakfast', 'Candy', 'Canned & Packaged', 'Cleaning Products',
                                     'Condiments & Sauces', 'Dairy', 'Deli', 'Electronics', 'Frozen', 'Garden & Patio',
                                     'General', 'Gift Cards', 'Hardware', 'Health', 'Health & Beauty', 'Home Decor',
                                     'International', 'Kitchen', 'Meat & Seafood', 'Natural & Organic', 'Other',
                                     'Pasta Sauces Grain', 'Personal Care', 'Pet Care', 'Produce', 'Snacks', 'Tobacco',
                                     'Travel & Luggage']

global selected_departments
selected_departments = []

standard_time = 0.2
alternate_time = 0.5
nonStandard_time = 1.5
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


############~~~~~~~ Find Google Chrome.EXE~~~~~~~############

def find_chrome_directory(starting_directories=possible_directories):
    # Define the name of the Chrome executable
    chrome_executable = "chrome.exe"  # Adjust for macOS and Linux if needed

    # Recursively search for Chrome in all directories
    for starting_directory in starting_directories:
        for foldername, subfolders, filenames in os.walk(starting_directory):
            if chrome_executable in filenames:
                # Chrome executable found, return its directory
                chrome_directory = os.path.join(foldername, chrome_executable)
                return chrome_directory

    print("Google Chrome not found.")
    return None


chrome_directory = find_chrome_directory()
if chrome_directory:
    print(f"The current directory of Google Chrome is: {chrome_directory}")


############~~~~~~~ Find Google Chrome Profile Path ~~~~~~~############
def find_chrome_profile_dir(starting_directory="C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome"):
    chrome_profile = "User Data"
    # Substitute the {user} variable with the actual username
    starting_directory = starting_directory.format(user=os.getlogin())
    # Search for Chrome profile in all directories
    for folder_name, sub_folders, fil_enames in os.walk(starting_directory):
        if chrome_profile in sub_folders:
            # If Chrome profile found, return its directory
            global chrome_profile_directory
            chrome_profile_directory = os.path.join(folder_name, chrome_profile)
            print("this is the directory: " + str(chrome_profile_directory))
            return chrome_profile_directory
    print("Google Chrome profile not found.")
    return None


############~~~~~~~ Find Google Chrome Profile ~~~~~~~############
def find_chrome_profile():
    global directory_locations
    directory_locations = []
    for i in possible_profile_names:
        for folder_name, sub_folders, file_names in os.walk(chrome_profile_directory):
            if i in sub_folders:
                global profile_name
                profile_name = i
                print(f"Profile found: {i}")
                directory_locations.append(os.path.join(folder_name, i))
                pass
    print(*directory_locations, sep='\n')


############~~~~~~~ Run the pre-configs ~~~~~~~############

find_chrome_profile_dir()
find_chrome_directory()
find_chrome_profile()

############~~~~~~~ Modify pathing for insertion later ~~~~~~~############

modified_chrome_profile_directory = re.sub(r'\\', r'\\\\', chrome_profile_directory)
modified_chrome_directory = re.sub(r'\\', r'\\\\', str(chrome_directory))
print(modified_chrome_profile_directory)
print(modified_chrome_directory)

############~~~~~~~ Start Selenium Options ~~~~~~~############

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--flag-switches-begin")
chrome_options.add_argument("--flag-switches-end")
chrome_options.add_argument("--origin-trial-disabled-features=WebGPU")
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("excludeSwitches", ["test-type"])
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = str(modified_chrome_directory)
userdatadir = str(modified_chrome_profile_directory)
userdatadir.format(user=os.getlogin())
profile_directory = str(profile_name)
chrome_options.add_argument(f"--user-data-dir={userdatadir}")
chrome_options.add_argument(f'--profile-directory={profile_directory}')
# chrome_options.add_argument('--incognito')
driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")



############~~~~~~~                              ~~~~~~~############
############~~~~~~~        Store Select          ~~~~~~~############
############~~~~~~~                              ~~~~~~~############
############~~~~~~~                              ~~~~~~~############

def store_selection():

    stores = [
        ("Kroger", "https://www.kroger.com/savings/cl/coupons"),
        ("Giant Eagle", None),  # Add the appropriate URL or function
        ("Target", None),       # Add the appropriate URL or function
        ("Ralphs", "https://www.ralphs.com/savings/cl/coupons"),
        ("King Soopers", "https://www.kingsoopers.com/savings/cl/coupons"),
        ("Food 4 Less", "https://www.food4less.com/savings/cl/coupons/"),
        ("Baker's", "https://www.bakersplus.com/savings/cl/coupons/"),
        ("City Market", "https://www.citymarket.com/savings/cl/coupons/"),
        ("Dillons", "https://www.dillons.com/savings/cl/coupons/"),
        ("Foods Co", "https://www.foodsco.net/savings/cl/coupons/"),
        ("Fred Meyer", "https://www.fredmeyer.com/savings/cl/coupons/"),
        ("Fry\'s", "https://www.frysfood.com/savings/cl/coupons/"),
        ("Gerbes", "https://www.gerbes.com/savings/cl/coupons/"),
        ("Jay C Food Store", "https://www.jaycfoods.com/savings/cl/coupons/"),
        ("Mariano\'s", "https://www.marianos.com/savings/cl/coupons/"),
        ("Metro Market", "https://www.metromarket.net/savings/cl/coupons/"),
        ("Pay-Less Super Markets", "https://www.pay-less.com/savings/cl/coupons/"),
        ("Pick\'n Save", "https://www.picknsave.com/savings/cl/coupons/"),
        ("QFC", "https://www.qfc.com/savings/cl/coupons/"),
        ("Smith\'s Food and Drug", "https://www.smithsfoodanddrug.com/savings/cl/coupons/"),
        ("Winn Dixie", "https://www.winndixie.com/coupons")

        # Add more store names and URLs as needed
    ]

    def create_button(text, command):
        return customtkinter.CTkButton(master=window, text=text, command=command)

    def on_store_click(url, name):
        window.destroy()
        if url:
            wait_for_sign_on(url, name)
        elif name == "Target":
            scroll_target()
        elif name == "Giant Eagle":
            GE_wait_for_sign_on()
        elif name == "Winn Dixie":
            winn_dixie_start()
        else:
            # Handle other actions or functions if needed
            print(f"Clicked {name}")

    window = customtkinter.CTk()
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    window.title("Sign on verification")
    window.minsize(400, 200)
    window.maxsize(1000, 1000)
    window.geometry("500x300")

    custom_font = customtkinter.CTkFont(family="<Ariel>", size=14)

    text = customtkinter.CTkLabel(master=window, text="Select the store to clip coupons from.", font=custom_font)
    text.pack()

    buttons = []
    for idx, (name, url) in enumerate(stores, start=1):
        command = lambda n=name, u=url: on_store_click(u, n)
        button = create_button(name, command)
        button.place(relx=(0.15 + (idx - 1) % 3 * 0.3), rely=(0.3 + (idx - 1) // 3 * 0.1), anchor=CENTER)
        buttons.append(button)

    window.mainloop()

# Call the function
def wait_for_sign_on(store_url, store_name):
    max_retries = 10
    current_retry = 0
    driver.get(store_url)
    sign_on(store_name)
    time.sleep(3)
#    button_xpath = f"//a[@class='kds-Link kds-Link--s kds-Link--implied p-8 block text-neutral-most-prominent' and text()='Digital Coupons']"
#    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, button_xpath))).click()


def scroll(store_name):
    if store_name == "Winn Dixie":
        winn_dixie_scroll()
    time.sleep(standard_time)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        time.sleep(alternate_time)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(alternate_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            click_coupons()
        last_height = new_height

def click_coupons():
    time.sleep(alternate_time)
    buttons = driver.find_elements(By.XPATH, '//button[starts-with(@data-testid, "CouponActionButton-")]')
    for button in buttons:
        ActionChains(driver).move_to_element(button).perform()
        button.click()
        kroger_too_many_coupons = None
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="ButtonFeedbackErrorMessage"]')))

            # Find the element after waiting
            too_many_coupons = driver.find_element(By.CSS_SELECTOR, '[data-testid="ButtonFeedbackErrorMessage"]')
            print("Maximum coupons clipped message detected.")
            if too_many_coupons:
                clicked_too_many_coupons()
                break
        except Exception as e:
            print(f"Error occurred: {e}")

        time.sleep(alternate_time)  # Add a small delay between clicks

def not_signed_on(store_name):
    print(f"not signed on {store_name}")

    def on_okay_click():
        window.destroy()
        driver.quit()
        sys.exit(1)

    window = customtkinter.CTk()
    window.title("Too many coupons")
    window.minsize(400, 200)
    window.maxsize(1000, 1000)
    window.geometry("400x200")

    text = customtkinter.CTkLabel(master=window, text="You need to sign on before we can clip coupons.")
    text.pack()
    button = customtkinter.CTkButton(master=window, text="Okay", command=on_okay_click)
    button.pack()
    window.mainloop()

def sign_on(store_name):
    def on_yes_click():
        window.destroy()
        if store_name == "Winn Dixie":
            winn_dixie_scroll()
        else:
            select_departments()

    def on_no_click():
        window.destroy()
        not_signed_on(store_name)

    window = customtkinter.CTk()
    window.title("Sign on verification")
    window.minsize(400, 200)
    window.maxsize(1000, 1000)
    window.geometry("400x200")

    text = customtkinter.CTkLabel(master=window, text=f"Are you logged into your {store_name} account?")
    text.pack()
    text2 = customtkinter.CTkLabel(master=window, text="If you are not, please sign in and click \"Yes\"")
    text2.pack()

    button = customtkinter.CTkButton(master=window, text="Yes", height=3, width=6, command=on_yes_click)
    button2 = customtkinter.CTkButton(master=window, text="No", height=3, width=6, command=on_no_click)
    button.pack()
    button2.pack()

    window.mainloop()

def on_checkbox_click():
    global selected_departments
    selected_departments = [list_of_departments[i] for i, value in enumerate(checkbox_vars) if value.get()]

def select_departments():
    window = customtkinter.CTk()
    custom_font = customtkinter.CTkFont(family="<Ariel>", size=14, )
    window.title("Select Departments")
    window.minsize(500, 500)
    window.maxsize(1000, 1000)
    window.geometry("550x550")
    global checkbox_vars
    checkbox_vars = [customtkinter.BooleanVar() for _ in list_of_departments]
    checkboxes_per_row = 3

    label_row = 0
    label_column = 0
    label_columnspan = checkboxes_per_row
    label = customtkinter.CTkLabel(master=window,
                                   text="If you would like to select specific departments, please select them below.\nOtherwise click \"Confirm department selection.\"",
                                   font=custom_font)
    label.grid(row=label_row, column=label_column, columnspan=label_columnspan, pady=10)
    for index, department in enumerate(list_of_departments):
        checkbox = customtkinter.CTkCheckBox(master=window, text=department, variable=checkbox_vars[index],
                                             command=on_checkbox_click)
        row = (index // checkboxes_per_row) + 1  # Start from row 1 for checkboxes
        checkbox.grid(row=row, column=index % checkboxes_per_row, sticky=W, padx=5, pady=5)

    button_row = (len(list_of_departments) - 1) // checkboxes_per_row + 2
    button_column = 0
    button_columnspan = checkboxes_per_row
    button = customtkinter.CTkButton(window, text="Confirm department selection.",
                                     command=lambda: [window.destroy(), department_selections()])
    button.grid(row=button_row, column=button_column, columnspan=button_columnspan, pady=10)

    window.mainloop()

def department_selections():
    print(selected_departments)
    if len(selected_departments) == 0:
        print("Nothing selected")
        scroll()
    else:
        click_department_selections()

def click_department_selections():
    print("Clicking selected departments")
    print(selected_departments)
    try:
        for i in selected_departments:
            try:
                selection = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                f"//span[@class='kds-Text--m truncate' and text()='{i}']")))

                time.sleep(alternate_time)

                # Scroll to the element using JavaScript
                ActionChains(driver).move_to_element(selection)
                time.sleep(nonStandard_time)
                selection.click()
            except TimeoutException as e:
                print(f"We couldn't find that department. Coupons may not exist for it. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    scroll()
def clicked_too_many_coupons():
    def on_click():
        window.destroy()
        driver.quit()
        sys.exit(1)

    def more_clipping():
        window.destroy()
        store_selection()

    window = customtkinter.CTk()
    window.title("Too many coupons")
    window.minsize(400, 200)
    window.maxsize(1000, 1000)
    window.geometry("400x200")

    text = customtkinter.CTkLabel(master=window, text="You\'ve clipped too many coupons!")
    text.pack()
    text2 = customtkinter.CTkLabel(master=window, text="We're stopping here.")
    text2.pack()
    button = customtkinter.CTkButton(master=window, text="Okay", command=on_click)
    button.pack()
    text3 = customtkinter.CTkLabel(master=window, text="Did you want to clip coupons from another site?")
    text3.pack()
    button2 = customtkinter.CTkButton(master=window, text="Let\'s clip more!", command=more_clipping)
    button2.pack()
    window.mainloop()


############~~~~~~~                              ~~~~~~~############
############~~~~~~~        Target Start          ~~~~~~~############
############~~~~~~~                              ~~~~~~~############
############~~~~~~~                              ~~~~~~~############


############~~~~~~~ Target Click on Coupons ~~~~~~~############

def click_coupons_target():
    print("Getting ready to click coupons.")  # used for debugging purposes
    try:
        # Scroll down to load more content
        driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "styles__StyledBaseButtonInternal") '
                                                      'and contains(@aria-label, "Save offer")]'))
        )
    except Exception as e:
        print(f"Error scrolling or finding buttons: {e}")
        return

    print("Finding and clicking buttons")  # used for debugging purposes
    coupon_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//div[contains(@class, "styles__OfferGridContainer-sc-1vf9v7z-0 ZzYoU")]'
                       '//button[contains(@class, "styles__StyledBaseButtonInternal") '
                       'and contains(@aria-label, "Save offer:")]'))
    )

    for button in coupon_buttons:
        try:
            # Scroll to the button
            ActionChains(driver).move_to_element(button).perform()
            button.click()

        except ElementClickInterceptedException as e:
            print("Too many coupons clipped.")
            clicked_too_many_coupons()
            breakpoint()

            time.sleep(0.1)
        except StaleElementReferenceException:
            print("Stale element reference. Retrying...")
            continue
        except Exception as e:
            print(f"Error: {e}")


############~~~~~~~ Target Scrolling ~~~~~~~############
def scroll_target():
    print("Scrolling")
    driver.get("https://www.target.com/circle/offers")
    target_sign_on()  # Moves to TKinter window to verify sign on
    while True:
        time.sleep(0.1)
        try:
            load_more_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//button[contains(@class, "styles__StyledBaseButtonInternal") and contains(text(), "Load more")]'))
            )
            load_more_button.click()
            time.sleep(0.1)
            new_height = driver.execute_script("return document.body.scrollHeight")

        except TimeoutException:
            # TimeoutException will be raised if the button is not present
            print("No more 'Load more' button. Stopping scrolling.")
            break

        except Exception as e:
            print(f"Error: {e}")
            break  # Break out of the loop if an error occurs

    click_coupons_target()


############~~~~~~~ Target sign On Verification ~~~~~~~############
def target_sign_on():
    def on_yes_click():
        window.destroy()

    def on_no_click():
        window.destroy()
        not_signed_on()
        sys.exit(1)  # Exit the entire program on "No" click

    window = customtkinter.CTk()
    window.title("Sign on verification")
    window.minsize(400, 200)
    window.maxsize(1000, 1000)
    window.geometry("400x200")

    text = customtkinter.CTkLabel(master=window, text="Are you logged into your Target account?")
    text.pack()

    button = customtkinter.CTkButton(master=window, text="Yes", height=3, width=6, command=on_yes_click)
    button2 = customtkinter.CTkButton(master=window, text="No", height=3, width=6, command=on_no_click)
    button.pack()
    button2.pack()

    window.mainloop()

############~~~~~~~                              ~~~~~~~############
############~~~~~~~     Giant Eagle Start        ~~~~~~~############
############~~~~~~~                              ~~~~~~~############
############~~~~~~~                              ~~~~~~~############

############~~~~~~~ Giant Eagle sign on check ~~~~~~~############

def GE_wait_for_sign_on():
    driver.get('https://www.gianteagle.com/')
    GE_sign_on()


############~~~~~~~ Verify Signed on ~~~~~~~############

def GE_sign_on():
    def on_yes_click():
        driver.get(
            'https://www.gianteagle.com/coupons')
        time.sleep(2)
        window.destroy()  # Close the window or perform other actions on "Yes" click
        GE_click_coupons()

    def on_no_click():
        window.destroy()
        not_signed_on()

    window = customtkinter.CTk()
    window.title("Sign on verification")
    window.minsize(400, 200)
    window.maxsize(1000, 1000)
    window.geometry("400x200")

    text = customtkinter.CTkLabel(master=window, text="Are you logged into your Giant Eagle account?")
    text.pack()
    text2 = customtkinter.CTkLabel(master=window, text="If you are not, please sign in and click \"Yes\"")
    text2.pack()

    button = customtkinter.CTkButton(master=window, text="Yes", height=3, width=6, command=on_yes_click)
    button2 = customtkinter.CTkButton(master=window, text="No", height=3, width=6, command=on_no_click)
    button.pack()
    button2.pack()

    window.mainloop()


############~~~~~~~ Click Coupons ~~~~~~~############

def GE_click_coupons():
    print("Getting ready to debug coupons")
    # Find all "Clip Coupon" elements
    clip_coupon_elements = driver.find_elements(By.XPATH,
                                                '//div[@class="sc-hygaQO GrPUA" and text()="Clip Coupon"]')

    # Iterate through the found elements and move the pointer to each location
    for clip_coupon_element in clip_coupon_elements:
        try:
            # Locate the element inside the loop to avoid stale element reference
            clip_coupon_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="sc-hygaQO GrPUA" and text()="Clip Coupon"]'))
            )

            # Move to the location of the "Clip Coupon" element
            driver.execute_script("arguments[0].scrollIntoView();", clip_coupon_element)

            # Click the "Clip Coupon" element
            clip_coupon_element.click()

            # Optionally, you can add a delay or other actions after each move
            time.sleep(alternate_time)

        except TimeoutException as e:
            # Handle exceptions if needed
            print(f"Error clicking Clip Coupon element: {str(e)}")
            print("No coupons to clip")

    try:
        # Wait for the page to load (adjust timeout as needed)
        coupon_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="CouponCatalogButton"]'))
        )

    except TimeoutException:
        print("No coupons found")
        GE_no_coupons_to_clip()

    GE_finished_coupons()


def GE_finished_coupons():
    def on_click():
        window.destroy()
        driver.quit()
        sys.exit(1)

    def more_clipping():
        window.destroy()
        store_selection()

    window = customtkinter.CTk()
    window.title("Too many coupons")
    window.minsize(400, 200)
    window.maxsize(1000, 1000)
    window.geometry("400x200")

    text = customtkinter.CTkLabel(master=window, text="Finished clipping. Closing your browser")
    text.pack()
    text2 = customtkinter.CTkLabel(master=window, text="We're stopping here.")
    text2.pack()
    button = customtkinter.CTkButton(master=window, text="Okay", command=on_click)
    button.pack()
    text3 = customtkinter.CTkLabel(master=window, text="Did you want to clip coupons from another site?")
    text3.pack()
    button2 = customtkinter.CTkButton(master=window, text="Let\'s clip more!", command=more_clipping)
    button2.pack()
    window.mainloop()


def GE_no_coupons_to_clip():
    def on_click():
        window.destroy()
        driver.quit()
        sys.exit(1)

    def more_clipping():
        window.destroy()
        store_selection()

    window = customtkinter.CTk()
    window.title("Too many coupons")
    window.minsize(400, 200)
    window.maxsize(1000, 1000)
    window.geometry("400x200")

    text = customtkinter.CTkLabel(master=window, text="Looks like we didn't have any coupons to clip.")
    text.pack()
    text2 = customtkinter.CTkLabel(master=window, text="We're stopping here.")
    text2.pack()
    button = customtkinter.CTkButton(master=window, text="Okay", command=on_click)
    button.pack()
    text3 = customtkinter.CTkLabel(master=window, text="Did you want to clip coupons from another site?")
    text3.pack()
    button2 = customtkinter.CTkButton(master=window, text="Let\'s clip more!", command=more_clipping)
    button2.pack()

    window.mainloop()



############~~~~~~~                              ~~~~~~~############
############~~~~~~~     Winn Dixie Start         ~~~~~~~############
############~~~~~~~                              ~~~~~~~############
############~~~~~~~                              ~~~~~~~############

############~~~~~~~    Winn Dixie sign on check  ~~~~~~~############

winn_dixie_clicked_coupons = set()

def winn_dixie_start(store_name):
    driver.get("https://www.winndixie.com/coupons")
    sign_on(store_name)


############~~~~~~~    Winn Dixie coupon click  ~~~~~~~############

def winn_dixie_coupon_click():
    print("Attempting to clip")
    time.sleep(2)

    try:
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[id^='cpnBtn_']"))
        )

        if not buttons:
            print("No buttons found with the specified criteria.")
            breakpoint()

        for button in buttons:
            coupon_id = button.get_attribute('id')

            try:
                button.click()
                time.sleep(1)
                print(f"Button with ID {coupon_id} clicked successfully!")
                winn_dixie_clicked_coupons.add(coupon_id)  # Add clicked coupon to the set

            except Exception as ex:
                print(f"Exception encountered while clicking the button with ID {coupon_id}: {ex}")

        if coupon_id in winn_dixie_clicked_coupons:
            print(f"Coupon with ID {coupon_id} has already been attempted.")
            clicked_too_many_coupons()
            return  # Exit the function since we've found a clicked coupon

    except TimeoutException:
        print("Timed out waiting for elements to be present.")
    except Exception as e:
        print(f"An error occurred: {e}")

############~~~~~~~    Winn Dixie scroll function  ~~~~~~~############

def winn_dixie_scroll():
    time.sleep(standard_time)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        time.sleep(alternate_time)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(alternate_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, 0);")
            winn_dixie_coupon_click()
        last_height = new_height


store_selection()
