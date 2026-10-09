import requests
import json

url = "http://localhost:8000/estimate/single"

print("Testing Improved Model with Different Stories\n")
print("=" * 60)

# Story 1: Simple UI (low complexity)
story1 = {
    "title": "Crear pantalla de login",
    "description": "Interfaz de login básica con username y password",
    "acceptance_criteria": None,
    "priority": None,
    "issue_type": None
}

response1 = requests.post(url, json=story1)
result1 = response1.json()
points1 = result1['point_estimate']['ensemble']
time1 = result1['time_estimate']['ensemble']
cost1 = result1['cost_estimate']['ensemble']
effort1 = result1['effort_estimate']['ensemble']

print(f"\nStory 1 (Simple UI): {story1['title']}")
print(f"  Points: {points1}, Time: {time1:.1f} days, Cost: ${cost1:.0f}, Effort: {effort1:.1f}h")

# Story 2: Complex Integration (high complexity)
story2 = {
    "title": "Integrar API de pagos Stripe",
    "description": "Sistema complejo de pagos que integra con Stripe. Requiere soporte para múltiples métodos de pago, manejo robusto de webhooks, reintentos automáticos en caso de fallo, logging detallado de todas las transacciones, monitoreo en tiempo real, tests unitarios completos y tests de integración. Arquitectura escalable y segura.",
    "acceptance_criteria": None,
    "priority": None,
    "issue_type": None
}

response2 = requests.post(url, json=story2)
result2 = response2.json()
points2 = result2['point_estimate']['ensemble']
time2 = result2['time_estimate']['ensemble']
cost2 = result2['cost_estimate']['ensemble']
effort2 = result2['effort_estimate']['ensemble']

print(f"\nStory 2 (Complex Integration): {story2['title']}")
print(f"  Points: {points2}, Time: {time2:.1f} days, Cost: ${cost2:.0f}, Effort: {effort2:.1f}h")

# Story 3: Bug fix (low complexity)
story3 = {
    "title": "Corregir validación de email",
    "description": "Pequeño bug en la validación del campo email del formulario de registro",
    "acceptance_criteria": None,
    "priority": None,
    "issue_type": None
}

response3 = requests.post(url, json=story3)
result3 = response3.json()
points3 = result3['point_estimate']['ensemble']
time3 = result3['time_estimate']['ensemble']
cost3 = result3['cost_estimate']['ensemble']
effort3 = result3['effort_estimate']['ensemble']

print(f"\nStory 3 (Bug Fix): {story3['title']}")
print(f"  Points: {points3}, Time: {time3:.1f} days, Cost: ${cost3:.0f}, Effort: {effort3:.1f}h")

print("\n" + "=" * 60)
print("[RESULTADO DEL TEST]")
print("=" * 60)

if points1 != points2 and points2 != points3 and points1 != points3:
    print("[OK] Las estimaciones son DIFERENTES - Modelo mejora funcionando!")
    print(f"\n  Story 1 (Simple):     {points1:.1f} pts")
    print(f"  Story 2 (Complex):    {points2:.1f} pts")
    print(f"  Story 3 (Bug):        {points3:.1f} pts")
    print(f"\n  Conclusión: El modelo ahora discrimina correctamente")
    print(f"  entre historias de diferente complejidad")
else:
    print(f"[ERROR] Resultados: {points1}, {points2}, {points3}")
    print(f"  Algunas historias tienen el mismo valor!")

# Verify time is also different
if time1 != time2 and time2 != time3:
    print(f"\n[OK] Duración también varía: {time1:.1f}, {time2:.1f}, {time3:.1f} días")
else:
    print(f"\n[INFO] Duración: {time1:.1f}, {time2:.1f}, {time3:.1f} días")

# Verify cost is also different
if cost1 != cost2 and cost2 != cost3:
    print(f"[OK] Costo también varía: ${cost1:.0f}, ${cost2:.0f}, ${cost3:.0f}")
else:
    print(f"[INFO] Costo: ${cost1:.0f}, ${cost2:.0f}, ${cost3:.0f}")

# Verify effort is also different
if effort1 != effort2 and effort2 != effort3:
    print(f"[OK] Esfuerzo también varía: {effort1:.1f}, {effort2:.1f}, {effort3:.1f}h")
else:
    print(f"[INFO] Esfuerzo: {effort1:.1f}, {effort2:.1f}, {effort3:.1f}h")
