import requests
from bs4 import BeautifulSoup
import csv

# 目标排名网站（以软科中国大学排名为例，可根据实际目标站调整）
base_url = "https://www.shanghairanking.cn/rankings/best-universities-in-china"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 存储所有大学数据
universities = []

# 分页爬取（假设每页展示一定数量，需根据实际网站调整分页逻辑）
page = 1
while True:
    # 构造分页URL（不同网站分页参数不同，需自行适配）
    url = f"{base_url}?page={page}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        break  # 无更多页面则退出

    soup = BeautifulSoup(response.text, "html.parser")
    # 定位大学信息的行（需根据目标网站的HTML结构调整选择器）
    rows = soup.select("table tr")[1:]  # 跳过表头行
    if not rows:
        break  # 无数据则退出

    for row in rows:
        cols = row.select("td")
        if len(cols) < 3:
            continue
        # 提取排名、名称、总分（字段需根据目标网站调整）
        rank = cols[0].get_text(strip=True)
        name = cols[1].get_text(strip=True)
        score = cols[2].get_text(strip=True)
        universities.append({"rank": rank, "name": name, "score": score})

    print(f"已爬取第{page}页，累计{len(universities)}条数据")
    page += 1
    # 若已爬取近600条，提前终止（可选）
    if len(universities) >= 600:
        break

# 将数据保存为CSV文件
with open("university_ranking.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["rank", "name", "score"])
    writer.writeheader()
    writer.writerows(universities)

print(f"爬取完成！共获取{len(universities)}所大学信息，已保存至university_ranking.csv")# 在这里编写代码
