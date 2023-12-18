# Digital CouponClipper

Clipping coupons for Kroger / Giant Eagle/ Target

Coupon clipper is run through Selenium webdriver. The program automatically selects your default Google Chrome profile and then presents the user with a pop-up notification asking which website you would like to clip coupons from. 

Since CouponClipper uses the default Google Chrome profile as the driver when clipping coupons, you must ensure that you have closed your Google Chrome broser, if it is actively being used, before running the program. **If you do not close your Google Chrome browser prior to running the program, it will crash**. Additionally, while it might be tempting to use the browser while the program is running, it is best not to touch anything on the webpage unless it's to log in or type in your password while the "are you signed in" pop-up is active. 

For Giant Eagle and Target, the program uses your defualt browser, it's very likely that if you had signed in previously, you will be able to just move forward. Kroger, on the other hand, has measures in place attempting to mitigate bot traffic. As a reuslt, you will likely need to sign in using your password before clipping coupons on the Kroger website. 

At present moment, Kroger is the only website that has the capabilities of being more target. E.g., You can select specific departments that you would like to clip coupons from. Once your selections have been made, the bot will select the same items you did, and then begin clipping coupons. However, if you choose not to make any selections, the program will default and auto-run without any additional targeting of specific departments, brands, or items wihtin the digital coupon section. 

Once a store has been selected, Couponclipper navigates to your requested website, ensures that you are logged in, and then navigates to the websites digital coupon page. From there, CouponClipper begins clipping the digital coupons on that page. 

This project is currently in Beta testing phase. 

# Requirements:
• python3.8 or greater
• Selenium webdriver
• Windows Opperating System

# Post Alpha implementations to be considered:

• Addition of targeting specific departments for Kroger - **Added in "BetaBuild.py"**
• Addition of targeting specific brands/departments for Target
• Other websites/stores that offer digital coupons
