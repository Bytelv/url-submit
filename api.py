print("将最新的url提交到百度和bing")
os.system("git checkout gh-pages")
urls = []

# 生成url列表
ret = subprocess.run(
    "git rev-parse --short HEAD", stdout = subprocess.PIPE, stderr = subprocess.PIPE
)
if ret.returncode == 0:
    commit_id = str(ret.stdout, "utf_8").strip()
ret = subprocess.run(
    "git show --pretty="
    " --name-only " + commit_id,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
)
if ret.returncode == 0:
    changes = str(ret.stdout, "utf-8").split("\n")
for change in changes:
    if change.endswith(".html"): #change[: -10] 是为了去掉末尾的index.html
urls.append("https://blog.lvbyte.top/{}".format(change[: -10]))
else :
    print("subprocess run error:{}".format(ret.stderr))
else :
    print("subprocess run error:{}".format(ret.stderr))

print("本次提交的urls:", urls)

# 提交到bing
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Host": "ssl.bing.com",
}
data = {
    "siteUrl": "https://blog.lvbyte.top",
    "urlList": urls
}
response = requests.post(
    url = "https://www.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey=3889b830d26a4a4385f5f839f6853ccc",
    headers = headers,
    data = json.dumps(data)
)
print("bing的响应: ", response.content)

# 提交到百度
headers = {
    "User-Agent": "curl/7.12.1",
    "Host": "data.zz.baidu.com",
    "Content-Type": "text/plain"
}
response = requests.post(
    url = "http://data.zz.baidu.com/urls?site=your-site.com&token=d06OCskOVbIyJFC6",
    headers = headers,
    data = "\n".join(urls)
)
print("百度的响应: ", response.content)
