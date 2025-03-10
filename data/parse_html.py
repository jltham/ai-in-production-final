from bs4 import BeautifulSoup
import os


def extract_important_content_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for element in soup(["script", "style", "aside", "footer", "header", "nav", "button"]):
        element.decompose()

    main_content = soup.find_all("p")
    content = "\n".join([p.get_text() for p in main_content])

    return content


if __name__ == "__main__":
    file_paths = os.listdir("./data/reddragonai.com")

    for file_path in file_paths:
        with open("./data/reddragonai.com/" + file_path, "r") as fp:
            html_content = fp.read()

        important_content = extract_important_content_from_html(html_content)

        with open(f"./data/{file_path}.txt", "w+") as fp:
            fp.write(important_content)
