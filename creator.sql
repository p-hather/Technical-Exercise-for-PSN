create table if not exists creator as
    select
        Creator,
        sum(revenue) as total_revenue,
        count(productName) as product_count,
        sum(profit) as total_profit
    from
        product
    group by
        Creator