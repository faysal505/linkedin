from flask import Flask, render_template, request
import re
import requests


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')





@app.route('/sub', methods=['GET', 'POST'])
def sub():
    if request.method == 'POST':
        text = request.form['link']
        pattern = r"https://teraboxapp\.com/s/[^\s]+"
        links = re.findall(pattern, text)
        # links = text.split(" ")
        print(links)
        names = []
        for index, link in enumerate(links):
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"}
            create_link = f"https://terabox-test1.vercel.app/api?data={link}"
            direct_link = requests.get(create_link, headers=headers).json()['direct_link']
            response = requests.get(direct_link, stream=True)
            response.raise_for_status()
            file_name = f"static/video{index}.mp4"
            names.append(file_name)
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            print("Download complete.")
        print(len(names))
        return render_template("show.html", vid=names)

if __name__ == '__main__':
    app.run(debug=True)


# https://www.1024tera.com/sharing/link?surl=g8JFl_MqxwB4UlHhujtrfQ https://teraboxapp.com/s/1V8WLeu65eiiFNvri6HujEQ