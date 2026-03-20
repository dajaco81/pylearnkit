def init():
    print("import pylearnkit")
    print()
    print('tasks = pylearnkit.load("../tasks/tasks1.txt")')
    print()
    print("# your code goes here")
    print()
    print("pylearnkit.check(globals())")

def load(path):
    from ast import literal_eval
    with open("../tasks/" + path, "r") as f:
        return list(map(literal_eval, f))

def export(namespace):
    tasks = namespace["tasks"]
    repeats = namespace["repeats"]
    path = namespace["outpath"]
    with open(path, "w") as f:
        for name, info in tasks:
            q_func = namespace[f"{name}_q"]
            a_func = namespace[f"{name}_a"]
            for _ in range(repeats):
                item = {
                "name": name,
                "info": info,
                "payload": (q := q_func()),
                "answer": a_func(q)
                }
                f.write(f"{item}\n")

def check(namespace):

    def task_totals(tasks):
        totals = {}
        order = []
        for task in tasks:
            name = task["name"]
            if name not in totals:
                totals[name] = 0
                order.append(name)
            totals[name] += 1
        return order, totals

    def task_name_width(order):
        return max(len(name) for name in order)
    
    def run_checks(tasks, namespace, totals, order):
        results = {name: {"total": total, "correct": 0} for name, total in totals.items()}
        missing_task = None
        current_index = 0
        current_name = order[current_index]
        for task in tasks:
            name = task["name"]
            if name != current_name:
                if missing_task is not None:
                    break
                if results[current_name]["correct"] != totals[current_name]:
                    break
                current_index += 1
                current_name = order[current_index]
            if name not in namespace:
                missing_task = task
                break
            result = namespace[name](task["payload"])
            task["result"] = result
            if result == task["answer"]:
                results[name]["correct"] += 1
        return results, missing_task
    
    def print_results(order, results, name_width):
        for i, name in enumerate(order, start=1):
            stats = results[name]
            print(f"[{i:02}] {name:<{name_width}} {stats['correct']:>3}/{stats['total']:<3}  ", end="")
            print("ok" if stats["correct"] == stats["total"] else "fail")

    def print_missing_task(order, missing_task, name_width):
        print()
        completed = order.index(missing_task["name"])
        print(f"[{completed+1:02}] {missing_task['name']:<{name_width}}")
        print(f"info: {missing_task['info']}")
        print(f"example: {missing_task['payload']} -> {missing_task['answer']}")

    def print_failed_task(order, failed_task, name_width):
        print()
        completed = order.index(failed_task["name"])
        print(f"[{completed+1:02}] {failed_task['name']:<{name_width}} failed")
        print(f"info: {failed_task['info']}")
        print(
            f"example: {failed_task['payload']} -> {failed_task['answer']} "
            f"(got {failed_task['result']})"
        )

    tasks = namespace["tasks"]
    order, totals = task_totals(tasks)
    name_width = task_name_width(order)
    results, missing_task = run_checks(tasks, namespace, totals, order)
    fail_count = sum(1 for name in order if results[name]["correct"] != results[name]["total"])
    total_count = len(order)
    if missing_task is not None:
        print_missing_task(order, missing_task, name_width)
        print()
        print_results(order, results, name_width)
        return
    print_results(order, results, name_width)
    print()
    if fail_count:
        failed_task = next(task for task in tasks if task.get("result") != task["answer"])
        print_failed_task(order, failed_task, name_width)
        return
    print(f"All {total_count} implementations passed.")
