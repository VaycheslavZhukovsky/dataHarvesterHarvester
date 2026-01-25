from project.infrastructure.categories import categories_dict

SUBCATEGORIES = []
for category in categories_dict.items():
    # print(category[1]["sub_url"])
    for c in category[1]["sub_url"]:
        SUBCATEGORIES.append(c[1].split("/")[-2])
print(SUBCATEGORIES)