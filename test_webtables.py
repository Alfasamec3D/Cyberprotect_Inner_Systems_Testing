from playwright.sync_api import expect

#Названия столбцов
table_header=["#firstName","#lastName","#userEmail","#age","#salary","#department"]

#Строки для тестирования
row_ex=[["Jon","Snow","jon.snow@ex.com","20","15000","frkt"],
        ["Kal","El","kal.el@ex.com","25","20000","fpmi"],
        ["Ned","Stark","ned.stark@ex.com","30","25000","fopf"],
        ["Don","Kent","don.kent@ex.com","35","30000","falt"],
        ["Bruce","Wayne","bruce.wayne@ex.com","40","35000","fefm"],
        ["Tony","Stark","tony.stark@ex.com","45","40000","fpfe"],
        ["Zuck","Snyder","zuck.snyder@ex.com","50","45000","faki"],
        ["Sean","Bean","sean.bean@ex.com","55","50000","fbmf"]]
invalid_row=["","","svet@ex.c","a","b",""]

#Функция доавления новой строк
def add_row(page_m, row):
    page_m.click("#addNewRecordButton")

    #Заполнение граф
    for i in range(6):
        page_m.fill(table_header[i], row[i])
    page_m.click("#submit")

#Тест поиска строки
def test_search(page):
    page.fill("#searchBox", "Cierra")
    rows = page.locator(".rt-tbody .rt-tr-group").filter(has_text="Cierra")
    rows.wait_for()
    assert rows.count() == 1

#Тест добавления строки
def test_add_record(page):
    add_row(page,row_ex[0])
    assert row_ex[0][0] in page.locator("div.rt-tbody").inner_text()

#Тест редактировования строк
def test_edit_record(page):
    page.click("span[title='Edit']")
    page.fill(table_header[0], row_ex[0][0])
    page.click("#submit")
    assert row_ex[0][0] in page.locator("div.rt-tbody").inner_text()

#Тест реакции на некорректный ввод строки
def test_invalid_input(page):
    add_row(page, invalid_row)

    # Проверяем, что окно не закрылось
    assert page.is_visible("#submit"), f"Форма закрылась при некорректном вводе"

#Тест удаления строки 
def test_delete_record(page):
    first_row = page.locator("div.rt-tbody div.rt-tr-group").first
    name_before = first_row.inner_text()
    first_row.locator("span[title='Delete']").click()
    assert name_before not in page.locator("div.rt-tbody").inner_text()

#Тест сортировки строк
def test_sort(page):

    #Функция получения значений столбца 3 в установленном порядке
    def get_values():
        return[
            int(cell.inner_text())
            for cell in page.locator("div.rt-td:nth-child(3)").all()
            if cell.inner_text().strip().isdigit()
        ]

    original_values=get_values()
    assert len(original_values)>0, "Таблица пустая!"
    page.locator("div.rt-th:has-text('Age')").click()

    sorted_values=get_values()

    assert sorted_values==sorted(original_values), "Сортировка по Age не работает!"

    page.locator("div.rt-th:has-text('Age')").click()
    sorted_desc_values=get_values()

    assert sorted_desc_values == sorted(original_values, reverse=True), "Сортировка по Age (Desc) не работает!"

#Тест выбора количества отображаемых строк на 1 странице
def test_pagination(page):
    page.select_option("select[aria-label='rows per page']", "5")
    rows = page.locator("div.rt-tbody div.rt-tr-group")
    assert rows.count() <= 5

#Тест переключения страниц
def test_page_navigating(page):
   
    #Добавление строк для создания 2 страницы
    for row in row_ex:
        add_row(page,row)

    first_row_text_before = page.locator(".rt-tr-group").nth(0).inner_text()

    #Нажимаем "Next"
    page.locator("button:has-text('Next')").click()

    page.wait_for_timeout(1000)

    #Проверка изменения 1 строки
    first_row_text_after = page.locator(".rt-tr-group").nth(0).inner_text()

    assert first_row_text_before != first_row_text_after, "Переход на следующую страницу не сработал"
    
    #Нажимаем " previous"
    page.locator("button:has-text('Previous')").click()
    page.wait_for_timeout(1000)
    first_row_text_after = page.locator(".rt-tr-group").nth(0).inner_text()

    assert first_row_text_before== first_row_text_after

    #Ввод номера страницы
    input_box = page.locator("input[aria-label='jump to page']")
    input_box.fill("2")
    input_box.press("Enter")

    #Проверка номера страницы
    current_page = page.locator("input[aria-label='jump to page']").input_value()
    assert current_page == "2"

#Тест кнопки перехода на домащнюю страницу
def test_banner_redirects_to_home(page):
    header_link = page.locator("header a")
    expect(header_link).to_have_attribute("href", "https://demoqa.com")
    logo_img = header_link.locator("img")

    #Проверка правильности источника изображения
    expect(logo_img).to_have_attribute("src", "/images/Toolsqa.jpg")

    #Проверка видимости логотипа
    expect(logo_img).to_be_visible()

#Тест рекламы
def test_advertisement_visible(page):
    ad = page.locator("div[class*='Advertisement']")
    assert ad.is_visible()

    #Проверка ссылки у рекламы
    ad_link = ad.locator("a")
    assert ad_link.count() > 0