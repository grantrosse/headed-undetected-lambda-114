import undetected_chromedriver as uc
from pyvirtualdisplay import Display
from tempfile import mkdtemp
import os, time, json

def get_uc_driver():
        
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--single-process")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")    
    
    driver_executable_path = '/tmp/chromedriver'
    os.system(f'cp /opt/chromedriver {driver_executable_path}')
    os.chmod(driver_executable_path, 0o777)

    driver = uc.Chrome(options=options,browser_executable_path='/opt/chrome/chrome', driver_executable_path=driver_executable_path, version_main=114)#, use_subprocess=True)

    return driver  

      
def handler(event=None, context=None):
    print(event)
    print('--------------\n')
    
    try: 
        display = Display(visible=0, size=(1024, 768)) 
        display.start()
        time.sleep(5)
        driver = get_uc_driver()
        
        driver.get('http://checkip.amazonaws.com/')
        print(driver.page_source)
        
        return {
            'statusCode': 200,
            'body': json.dumps('OK')
        }
        
        
        
    except Exception as e: 
        print(f'error in main function: {e}')
        print('type is:', e.__class__.__name__)
    
        return {
            'statusCode': 200,
            'body': json.dumps({'error': f'{e}'})
        }
