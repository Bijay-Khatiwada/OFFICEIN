import random, json, uuid

def generate_fake_employees():
    employees_list = []
    for i in range(0, 5):
        _name  = "employee" + str(i)
        _age = random.randint(18,25)
        _email = _name + "@gmail.com"
        employees_list.append(
            { "name": _name, "age":_age, "email":_email, "position": []}
        )
    return employees_list

employees = generate_fake_employees()
print(employees)
fout = open("data.json", "w")
fout.write(json.dumps(employees))
fout.close()

    
