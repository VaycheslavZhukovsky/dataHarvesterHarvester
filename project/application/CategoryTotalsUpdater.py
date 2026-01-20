import asyncio


async def update_all_totals(page_category_total_products, paginators):
    tasks = []

    for parts, paginator in paginators.items():
        category_slug = paginator.parts.segments[1]
        total_products = paginator.total_products

        tasks.append(
            asyncio.create_task(
                page_category_total_products.update_total_products(
                    category_slug,
                    total_products
                )
            )
        )

    # Запускаем конкурентно
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Логируем ошибки
    for task_result, (parts, paginator) in zip(results, paginators.items()):
        if isinstance(task_result, Exception):
            print(f"Ошибка при обновлении {parts}: {task_result}")

    return results
