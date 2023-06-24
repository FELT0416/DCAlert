from bs4 import BeautifulSoup
import requests
import time
import re
import webbrowser
import zroya
import tkinter
import customtkinter
import os
import threading
import sys
import configparser
import winsound



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        key = []
        user = []
        self.url = ""
        self.check1 = 0
        self.check2 = 0
        self.config = configparser.ConfigParser()
        with open('settings.ini', 'r', encoding='utf-8') as file:
            self.config.read_file(file)
        if self.config.has_section("General"):
            self.url = self.config["General"]["url"]
            self.check1 = int(self.config["General"]["Checkbox1"])
            self.check2 = int(self.config["General"]["Checkbox2"])

            for i in self.config.options("Keywords"):
                key.append(str(self.config.get("Keywords", i)))
            for i in self.config.options("Username"):
                user.append(str(self.config.get("Username", i)))
            file.close()
        self.title("my app")
        self.geometry("400x280")
        self.resizable(False, False)
        self.copystate = 0
        self.soundstate = 0
        self.keywords = ()
        self.writers = ()
        self.copy = customtkinter.IntVar()
        self.sound = customtkinter.IntVar()
        self.articleurl=""
        rows = 4
        columns = 3
        for i in range(rows):
            self.grid_rowconfigure(i, weight=1)
        for i in range(columns):
            self.grid_columnconfigure(i, weight=1)

        self.gall_address = customtkinter.CTkEntry(master=self, placeholder_text="갤러리 주소 입력", height=35)
        self.gall_address.insert(0, self.url)
        self.gall_address.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.keyword_input = customtkinter.CTkEntry(master=self, placeholder_text="키워드/글작성자", height=35)
        self.keyword_input.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.input_keyword = customtkinter.CTkButton(master=self, text="키워드 추가",
                                                    command=lambda: self.add_to_listbox(self.keyword_list), width=100, corner_radius=0)
        self.input_keyword.grid(row=2, column=0)

        self.input_writer = customtkinter.CTkButton(master=self, text="사용자 추가",
                                                    command=lambda: self.add_to_listbox(self.writer_list), width=100, corner_radius=0)
        self.input_writer.grid(row=2, column=1)

        self.delete_selected = customtkinter.CTkButton(master=self, text="키워드 삭제",
                                                    command = lambda: self.remove_from_listbox(self.keyword_list), width = 100, corner_radius=0)
        self.delete_selected.grid(row=4, column=0)

        self.delete_selected = customtkinter.CTkButton(master=self, text="사용자 삭제",
                                                    command = lambda: self.remove_from_listbox(self.writer_list), width = 100, corner_radius=0)
        self.delete_selected.grid(row=4, column=1)

        self.checkbox_frame = customtkinter.CTkFrame(self, width=200)
        self.checkbox_frame.grid(row=1, column=2, columnspan=2, rowspan=3, sticky="news")

        self.title = customtkinter.CTkLabel(self.checkbox_frame, text="설정")
        self.title.grid(row=0, column=0, padx=5, pady=(5, 0), columnspan=2, sticky="nsew")

        self.keyword_frame = customtkinter.CTkFrame(self, width=100)
        self.keyword_frame.grid(row=3, column=0, rowspan=1)

        self.writer_frame = customtkinter.CTkFrame(self, width=100)
        self.writer_frame.grid(row=3, column=1, rowspan=1)

        self.toggle_app = customtkinter.CTkButton(master=self, text="시작", command=self.toggleapp, width=200, corner_radius=0)
        self.toggle_app.grid(row=4, column=3, sticky="ew")

        self.save_config = customtkinter.CTkButton(master=self, text="설정 저장", command=self.savesettings, width=200,
                                                  corner_radius=0)
        self.save_config.grid(row=3, column=3, sticky="s")

        self.checkbox_1 = customtkinter.CTkCheckBox(self.checkbox_frame, text="코드 복사하기                         ", variable=self.copy)
        self.checkbox_1.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        if self.check1:
            self.checkbox_1.select()

        self.checkbox_2 = customtkinter.CTkCheckBox(self.checkbox_frame, text="알림음 켜기", variable=self.sound)
        self.checkbox_2.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        if self.check2:
            self.checkbox_2.select()

        self.keyword_list = tkinter.Listbox(self.keyword_frame)
        self.keyword_list.pack()
        for i in key:
            self.keyword_list.insert(0, i)

        self.writer_list = tkinter.Listbox(self.writer_frame)
        self.writer_list.pack()
        for i in user:
            self.writer_list.insert(0, i)

    def savesettings(self):
        for i in self.config.sections():
            self.config.remove_section(i)
        self.keywords = self.keyword_list.get(0, tkinter.END)
        self.writers = self.writer_list.get(0, tkinter.END)
        self.config["General"] = {"url" : self.gall_address.get(),
                                  "Checkbox1" : self.checkbox_1.get(),
                                  "Checkbox2" : self.checkbox_2.get()}

        self.config["Keywords"] = {}
        self.config["Username"] = {}
        for i in range(len(self.keywords)):
            self.config["Keywords"][f"Keyword{str(i)}"] = self.keywords[i]
        for i in range(len(self.writers)):
            self.config["Username"][f"Username{str(i)}"] = self.writers[i]
        with open("settings.ini", "w", encoding="utf-8") as configfile:
            self.config.write(configfile)
            print("saved!")

    def check_url(self):
        pattern = r"https://gall.dcinside.com/(?:mgallery/)?board/lists(?:/)?\?id=(\w+)"
        match = re.match(pattern, self.gall_address.get())
        if not match:
            #self.open_window()
            return False
        else:
            return True

    #def open_window(self):
        #if self.error_window is None or not self.error_window.winfo_exists():
        #    self.error_window = ErrorWindow(self)
        #else:
        #    self.error_window.focus()

    def button_callback(self):
        print("button pressed") # For debug

    def add_to_listbox(self, listboxes):
        word=self.keyword_input.get()
        listboxes.insert(0, word)
        self.keyword_input.delete(0, customtkinter.END)

    def remove_from_listbox(self, listboxes):
        index=listboxes.curselection()
        if len(index)==0:
            listboxes.delete(tkinter.END)
        else:
            listboxes.delete(index)

    def toggleapp(self):
        global search_thread
        if self.toggle_app.cget("text") == "시작":
            while search_thread is not None and search_thread.is_alive():
                time.sleep(1)
            linkcheck = self.check_url()
            if not linkcheck:
                print("url 오류")
                return
            global soup
            self.url = self.gall_address.get()
            url = self.url
            session = requests.Session()
            session.headers.update({'User-Agent': 'Mozilla/5.0'})
            page = session.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            self.copystate = self.copy.get()
            self.soundstate = self.sound.get()
            self.keywords = self.keyword_list.get(0, tkinter.END)
            self.writers = self.writer_list.get(0, tkinter.END)
            self.articleurl=convert_url(self.url)
            search_thread = GallData()
            search_thread.start()
            self.toggle_app.configure(text="정지", fg_color="#d14b4b", hover_color="#9e2a2a")

        else:
            self.toggle_app.configure(text="시작", fg_color="#1f6aa5", hover_color="#144870")
            search_thread.stop()


def request_session(url):

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    while True:
        try:
            page = session.get(url)
            break
        except requests.RequestException:
            print("Internet connection lost")
            time.sleep(5)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup





def open_url(url):
    webbrowser.open_new_tab(url)


class GallData(threading.Thread):
    instance_running = False
    def __init__(self):
        super().__init__()
        if GallData.instance_running:
            raise RuntimeError("Another instance of MyClass is already running.")
        GallData.instance_running = True
        self.stop_flag = threading.Event()
        self.stop_flag.set()
        self.latestIndex=0
        self.latestTitle=""
        self.pageNum = []
        self.checkIndex=0
        self.soup=request_session(app.url)
        self.body=""
        self.stop_flag = threading.Event()
        self.stop_flag.set()
        self.checkRunning = True
        gnum = self.soup.find_all("td", attrs={'class': 'gall_num'})
        for i in gnum:
            self.pageNum.append(i.get_text())

        #latestIndex, pageNum1<인덱스 내림차순 정렬)
        self.pagenum1 = []
        for num in self.pageNum:
            if num.isnumeric():
                self.pagenum1.append(num)
        self.pageNum1 = [int(x) for x in self.pagenum1]
        self.pageNum1.sort(reverse=True)
        self.latestIndex=str(self.pageNum1[0])
        self.checkIndex=self.latestIndex

    def refresh(self):
        self.soup=request_session(app.url)

    def get_index(self):
        # pageNum(IndexList)
        self.pageNum=[]
        gnum = self.soup.find_all("td", attrs={'class': 'gall_num'})
        for i in gnum:
            self.pageNum.append(i.get_text())

        # latestIndex, pageNum1<인덱스 내림차순 정렬)
        self.pagenum1 = []
        for num in self.pageNum:
            if num.isnumeric():
                self.pagenum1.append(num)
        self.pageNum1 = [int(x) for x in self.pagenum1]
        self.pageNum1.sort(reverse=True)
        self.latestIndex = str(self.pageNum1[0])

    def get_writer(self):
        self.writers = []
        gwriter = self.soup.find_all(True, attrs={"class": ["gall_writer ub-writer"]})
        for i in gwriter:
            self.writers.append(i.get_text())

    def get_title(self):
        # TitleList
        self.titles = []
        gtitle = self.soup.find_all("td", attrs={'class': 'gall_tit ub-word'})
        for i in gtitle:
            title = i.get_text()
            title1 = title.splitlines()
            if len(title1) != 1:
                self.titles.append(title1[1])
            else:
                self.titles.append(title1[0])

        # LatestTitle
        indexcheck = self.pageNum.index(self.latestIndex)
        try:
            self.latestWriter = self.writers[indexcheck]
            self.latestTitle = self.titles[indexcheck]
        except:
            print(f"{len(self.titles)}, {indexcheck}")
            for i in self.pageNum:
                print(i)
            print(self.latestIndex)

    def check_keywords(self):
        check = False
        for i in app.keywords:
            if self.keyword_check(i):
                check = True
        return check

    def check_writers(self):
        check=False
        for i in app.writers:
            if self.writer_check(i):
                check = True
        return check

    def get_code(self):
        body = self.check_body()
        code = self.extract_code(body)
        addToClipBoard(code)
        print("code")
        return code

    def find_new(self):
        while not self.stop_flag.is_set():
            try:
                print("Looping")
                self.refresh()
                self.get_index()
                if self.latestIndex != self.checkIndex:
                    self.get_writer()
                    self.get_title()
                    self.checkIndex = self.latestIndex
                    if len(app.keywords) != 0 or len(app.writers) != 0:
                        check1 = self.check_keywords()
                        check2 = self.check_writers()
                        if check1 or check2:
                            if app.copystate == 1:
                                self.check_body()
                                code = self.get_code()
                                print(self.body)
                            notify(self.latestTitle, "", self.latestIndex)
                    else:
                        notify(self.latestTitle, "", self.latestIndex)

                print("searching")
                time.sleep(3)
                if self.stop_flag.is_set():
                    print("Stop")
                    GallData.instance_running = False
                    break
            except IndexError:
                continue

    def keyword_check(self, keyword):
        if keyword in self.latestTitle:
            return True
        else:
            return False

    def writer_check(self, writer):
        if writer in self.latestWriter:
            return True
        else:
            return False

    def check_body(self):
        page_url = f"{app.articleurl}{self.latestIndex}"
        bodySoup=request_session(page_url)
        self.body = bodySoup.find("div", attrs={'class': 'write_div'}).get_text()
        body = self.body.replace("-", "")
        return body

    def extract_code(self, body):
        substrings = re.split(r'\s+', body)
        code=""
        truefactor = 0
        for substring in substrings:
            if re.match(r'^(?=.*\d)[A-Za-z0-9]{8}$', substring):
                if truefactor == 0:
                    code = substring
                    truefactor = 1
                else:
                    if re.match(r'^[0-9]{8}$', substring):
                        code = substring
        return code

    def run(self):
        self.stop_flag.clear()
        self.find_new()

    def stop(self):
        self.stop_flag.set()
        self.join()


def on_closing():
    if search_thread is not None:
        search_thread.stop()
    app.destroy()


def notify(title, code, index):
    alert = zroya.Template(zroya.TemplateType.ImageAndText4)
    alert.setFirstLine(title)
    alert.setSecondLine(code)
    alert.setThirdLine("")
    url = f"{app.articleurl}{index}"

    def onClickHandler(notification_id):
        open_url(url)
    zroya.show(alert, on_click=onClickHandler)
    if app.checkbox_2.get():
        winsound.PlaySound("wav/notification1.wav", winsound.SND_FILENAME)


def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)


def convert_url(input_url):
    pattern = r"https://gall.dcinside.com/(?:mgallery/)?board/lists(?:/)?\?id=(\w+)"
    match = re.match(pattern, input_url)
    if match:
        gallery_id = match.group(1)
        output_url = f"https://gall.dcinside.com/{'mgallery/' if 'mgallery' in input_url else ''}board/view/?id={gallery_id}&no="
        return output_url
    return None


if __name__ == "__main__":
    status = zroya.init(
        app_name="DcAlert",
        company_name="FELT",
        product_name="DcAlert",
        sub_product="core",
        version="v01"
    )
    if not status:
        print("Initialization failed")
    search_thread = None
    customtkinter.set_appearance_mode("dark")
    app = App()
    appRunning = True
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()