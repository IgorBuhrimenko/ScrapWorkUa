import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.work.ua/jobs-python+junior/'


def get_soup(response):
    return BeautifulSoup(response.text, 'lxml')


def write_to_csv_file(filename, links):
    with open(filename, mode='w') as f:
        header = ['Name-Vacancy', 'Wage', 'Location', 'Description', 'Data Publication', 'URL']
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()

        for link in links:
            process_offer(writer, link)


def process_offer(writer, offer_link):
    response = requests.get(offer_link)
    soup = get_soup(response)
    name = soup.find('h1', attrs={'id': 'h1-name'})
    print(name.text)
    wage = soup.find('b')
    print(wage.text)
    adr = soup.find(class_='text-indent add-top-sm')
    adr_list = adr.text.split()
    location = ' '.join(adr_list)
    print(location)
    work_description = soup.find('div', attrs={'id': 'job-description'})
    print(work_description.text)
    data_publication = soup.find(class_='text-muted')
    print(data_publication.text)

    writer.writerow({
        'Name-Vacancy': name.text,
        'Wage': wage and wage.text,
        'Location': location ,
        'Description': work_description and work_description.text,
        'Data Publication': data_publication.text,
        'URL': offer_link
    })


response = requests.get(BASE_URL)
soup = get_soup(response)
work_tags = soup.find_all('h2')

work_links = []

for link in work_tags:
    if link.find('a') !=None:
        work_links.append(link)

links = []
for link in work_links:
    links.append(link.find('a').get('href').replace('/', 'https://www.work.ua/', 1))

write_to_csv_file('work-ua-python', links)
