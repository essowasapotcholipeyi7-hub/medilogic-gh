from db_helper import db

result = db.execute_query("SELECT id, nom, type_assurance, taux_prise_charge FROM patients")
for r in result:
    print(f"ID: {r['id']}, Assurance: {r['type_assurance']}, Taux: {r['taux_prise_charge']}")