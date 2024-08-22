import concurrent.futures

import boto3


dyn_resource = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    aws_access_key_id="A",
    aws_secret_access_key="B",
)

client = boto3.client(
    "dynamodb",
    region_name="us-east-1",
    aws_access_key_id="A",
    aws_secret_access_key="B",
)
table = dyn_resource.Table("forms-staging-db")


def get_all_items_parallel(segment, total_segments):
    items = []
    try:
        response = table.scan(Segment=segment, TotalSegments=total_segments)
        items.extend(response["Items"])
        while "LastEvaluatedKey" in response:
            response = table.scan(
                Segment=segment,
                TotalSegments=total_segments,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            items.extend(response["Items"])
    except Exception as e:
        raise Exception(f"Error retrieving items in segment {segment}: {e}")
    return items


def get_all_items_concurrently(total_segments=2):
    all_items = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=total_segments) as executor:
        futures = [
            executor.submit(get_all_items_parallel, segment, total_segments)
            for segment in range(total_segments)
        ]
        for future in concurrent.futures.as_completed(futures):
            all_items.extend(future.result())
    return all_items


def update_items(items):
    try:
        totals = len(items)
        with table.batch_writer() as batch:
            failed_count = 0
            for count, item in enumerate(items):
                if "created_at" in item and "creation_date" in item:
                    item["signed_at"] = item["created_at"]
                    item["signed_at_day"] = item["creation_date"]
                    batch.put_item(Item=item)
                else:
                    failed_count += 1
                if count % 100 == 0:
                    print(f"Items updated: {count}/{totals}")
        print(f"Items failed to update: {failed_count}")
        print("Items updated successfully.")
    except Exception as e:
        print(f"Error updating items: {e}")


def increase_provisioned_throughput(
    table_name, read_capacity_units, write_capacity_units
):
    current_settings = client.describe_table(TableName=table_name)
    current_read_capacity = current_settings["Table"]["ProvisionedThroughput"][
        "ReadCapacityUnits"
    ]
    current_write_capacity = current_settings["Table"]["ProvisionedThroughput"][
        "WriteCapacityUnits"
    ]
    print(f"Current Read Capacity Units: {current_read_capacity}")
    print(f"Current Write Capacity Units: {current_write_capacity}")
    # Update provisioned throughput settings
    response = client.update_table(
        TableName=table_name,
        ProvisionedThroughput={
            "ReadCapacityUnits": read_capacity_units,
            "WriteCapacityUnits": write_capacity_units,
        },
    )


# Increase provisioned throughput
# increase_provisioned_throughput("forms-staging-db", 50, 50)
items = get_all_items_concurrently()
print(len(items))
# print("start updating items...")
update_items(items)
