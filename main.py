import sys
import time
import socket
import warnings
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select


def check_date_format(date):
    if len(date) != 8:
        print("Error: Date must be in the format 'YYYYMMDD'.")
        return False
    elif not date.isdigit():
        print("Error: Date must contain only digits.")
        return False
    else:
        return True


def check_currency_code(currency_code):
    if not isinstance(currency_code, str):
        warnings.warn("Error: Currency code must be a string.", UserWarning)
        return False
    elif not currency_code.isalpha():
        warnings.warn("Error: Currency code must contain only letters.", UserWarning)
        return False
    else:
        return True


def check_internet_connection():
        try:
            # Attempt to create a socket connection to a well-known host
            socket.create_connection(("https://www.11meigui.com/tools/currency", 80))
            return True
        except OSError:
            pass
        return False




if __name__ == "__main__":

    # 网站URL
    exchange_rate_url = "https://www.11meigui.com/tools/currency"
    currency_reference_url = "https://www.11meigui.com/tools/currency"

    # 检查是否输入了所有三个参数
    if len(sys.argv) != 3:

        warnings.warn("参数编号不正确，应提供两个参数", UserWarning)
        print("例子: python3 file.py 20210905 USD")

        sys.exit()
    else:
        # 参数1：日期
        date = sys.argv[1]
        year = date[:4]
        month = date[4:6]
        day = date[6:8]

        # 参数1：货币
        currency_code = sys.argv[2]

        if check_date_format(date) and check_currency_code(currency_code.upper()):
            print("日期和货币代码都有效")


    if check_internet_connection():
        print("Internet connection is available.")
    else:
        print("No internet connection.")

    # 启动Chrome WebDriver的新实例
    driver = webdriver.Chrome()


    currency_table = {}

    try:
        # 转到新的URL
        driver.get("https://www.11meigui.com/tools/currency")

        # 查找id为“desc”的table元素
        table_element = driver.find_element(By.ID, "desc")
        if table_element:

            # 查找id为“desc”的table元素中的所有表
            tables = table_element.find_elements(By.TAG_NAME, "table")
            if tables:

                for table in tables:
                    # 查找table中的所有行
                    rows = table.find_elements(By.TAG_NAME, "tr")

                    # 循环遍历每个table，从第三个tr元素开始
                    for row in rows[1:]:
                        # Get the first and fifth value
                        columns = row.find_elements(By.TAG_NAME, "td")
                        if len(columns) >= 5:
                            second_value = columns[1].text
                            fifth_value = columns[4].text
                            currency_table[fifth_value] = second_value

        print(currency_table)

        # 导航到URL并等待页面完全加载
        driver.get("https://www.boc.cn/sourcedb/whpj/")
        time.sleep(6)

        # 在BOC网站上查找输入标签“
        start_date_input_element = driver.find_element(By.CSS_SELECTOR, "input#erectDate.search_ipt")
        end_date_input_element = driver.find_element(By.CSS_SELECTOR, "input#nothing.search_ipt")
        currency_input_element = driver.find_element(By.CSS_SELECTOR, "select#pjname")
        search_button = driver.find_element(By.CSS_SELECTOR, "input.search_btn:nth-child(1)")

        # 如果找到日历，则开始挑选日期如果找到日历，则开始挑选日期
        if start_date_input_element:
            driver.execute_script(f"document.getElementById('erectDate').value='{year}-{month}-{day}'")

        if end_date_input_element:
            driver.execute_script(f"document.getElementById('nothing').value='{year}-{month}-{day}'")

        if currency_input_element:
            dropdown = Select(currency_input_element)
            dropdown.select_by_value(currency_table[currency_code.upper()])
            search_button.click()

            print("found everything", currency_table[currency_code.upper()])
            time.sleep(3)

        # 查找所有行和表
        result_table = driver.find_elements(By.TAG_NAME, "table")
        if result_table:
            rows = result_table[1].find_elements(By.TAG_NAME, "tr")

            for row in rows[1:2]:
                # 获取行数据
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) >= 5:

                    answer = f"""
货币名称:{columns[0].text}
现汇买入价:{columns[1].text}
现钞买入价:{columns[2].text}
现汇卖出价:{columns[3].text}
现钞卖出价:{columns[4].text}
中行折算价:{columns[5].text}
发布时间:{columns[6].text}	
                """

            # 将数据写入文件
            with open("result.txt", "w") as file:
                file.write(answer)
                print("result.txt created")


    except TimeoutException:
        # 如果在指定的时间内找不到元素，则处理异常
        print("Element has not loaded yet or cannot be found")

    finally:
        # 关闭浏览器窗口
        time.sleep(2)
        driver.quit()

