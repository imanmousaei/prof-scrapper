import requests

from bs4 import BeautifulSoup


class University:
    def __init__(self, uni_url, faculty_url):
        self.uni_url = uni_url
        self.faculty_url = faculty_url

    # implement in children
    def scrape(self):
        return

    def get_google_scholar(self, prof_name):
        url_prof_name = prof_name.split(" ")[0] + "+" + prof_name.split(" ")[-1]
        url = f"https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors={url_prof_name}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        search_result = soup.find("div", class_="gsc_1usr")
        try:
            h3 = search_result.find("h3", class_="gs_ai_name")
            a_link = h3.find("a")
            href = a_link["href"]
            gs_url = f"https://scholar.google.com{href}"
            return gs_url
        except:
            return ""

    def scrape_email(self, url, suffix):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        email_elements = soup.find_all("a")
        for l in email_elements:
            try:
                href = l["href"]
                if "mailto" in href and "@" in l.text and suffix in l.text.lower():
                    return l.text
            except:
                pass


class Harvard(University):
    def __init__(self, *args, **kwargs):
        return super().__init__(uni_url="https://www.seas.harvard.edu", faculty_url="https://www.seas.harvard.edu/computer-science/faculty-research", *args, **kwargs)

    def scrape(self):
        page = requests.get(self.faculty_url)

        soup = BeautifulSoup(page.content, "html.parser")
        ai_element = soup.find("div", class_="accordion-content")
        profs = ai_element.find_all("span", class_="field-content")

        file = open("exports/harvard.csv", "a")
        file.write("prof name, google scholar, email")

        for p in profs:
            prof_name = p.text
            google_scholar = self.get_google_scholar(prof_name)

            href = p.find("a")["href"]
            prof_url = f"{self.uni_url}{href}"
            email = self.scrape_email(url=prof_url, suffix="harvard.edu")

            line = f"{prof_name}, {google_scholar}, {email} \n"
            file.write(line)

        file.close()