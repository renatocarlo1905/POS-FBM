'use strict';
const ORDER_DEMO={
  "asOf": "2026-09-26",
  "rows": [
    {
      "id": "SIM-APA-001",
      "kind": "layaway",
      "status": "pending",
      "branch": 2,
      "customer": {
        "name": "Cliente de prueba 01",
        "phone": "000 000 0001"
      },
      "created": "2026-09-23T12:00:00-06:00",
      "term": 45,
      "due": "2026-11-07",
      "ready": null,
      "total": 100000,
      "items": [
        {
          "name": "Anillo artesanal de muestra",
          "qty": 1,
          "price": 100000,
          "cost": 50000
        }
      ],
      "payments": [
        {
          "id": "SIM-APA-001-ANT",
          "kind": "Anticipo",
          "amount": 40000,
          "at": "2026-09-23T12:00:00-06:00",
          "branch": 2,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-09-23T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Registrado",
          "note": "Recepción y anticipo de ejemplo."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [
        "Melissa",
        "Jessica"
      ],
      "work": "",
      "expected_delivery": null,
      "budget_history": [],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": false
    },
    {
      "id": "SIM-APA-002",
      "kind": "layaway",
      "status": "pending",
      "branch": 1,
      "customer": {
        "name": "Cliente de prueba 02",
        "phone": "000 000 0002"
      },
      "created": "2026-08-17T12:00:00-06:00",
      "term": 45,
      "due": "2026-10-01",
      "ready": null,
      "total": 200000,
      "items": [
        {
          "name": "Anillo artesanal de muestra",
          "qty": 1,
          "price": 200000,
          "cost": 100000
        }
      ],
      "payments": [
        {
          "id": "SIM-APA-002-ANT",
          "kind": "Anticipo",
          "amount": 80000,
          "at": "2026-08-17T12:00:00-06:00",
          "branch": 1,
          "actor": "Melissa",
          "method": "Efectivo"
        },
        {
          "id": "SIM-APA-002-ABO",
          "kind": "Abono",
          "amount": 40000,
          "at": "2026-09-24T12:00:00-06:00",
          "branch": 2,
          "actor": "Ximena",
          "method": "Tarjeta · Banco de prueba · 1234"
        }
      ],
      "history": [
        {
          "at": "2026-08-17T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Registrado",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-24T12:00:00-06:00",
          "actor": "Ximena",
          "from": "Pendiente de pago",
          "to": "Abono",
          "note": "Cobro de ejemplo en sucursal 2"
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [
        "Melissa",
        "Jessica"
      ],
      "work": "",
      "expected_delivery": null,
      "budget_history": [],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": false
    },
    {
      "id": "SIM-APA-003",
      "kind": "layaway",
      "status": "pending",
      "branch": 2,
      "customer": {
        "name": "Cliente de prueba 03",
        "phone": "000 000 0003"
      },
      "created": "2026-08-07T12:00:00-06:00",
      "term": 45,
      "due": "2026-09-21",
      "ready": null,
      "total": 150000,
      "items": [
        {
          "name": "Anillo artesanal de muestra",
          "qty": 1,
          "price": 150000,
          "cost": 75000
        }
      ],
      "payments": [
        {
          "id": "SIM-APA-003-ANT",
          "kind": "Anticipo",
          "amount": 60000,
          "at": "2026-08-07T12:00:00-06:00",
          "branch": 2,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-08-07T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Registrado",
          "note": "Recepción y anticipo de ejemplo."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [
        "Melissa",
        "Jessica"
      ],
      "work": "",
      "expected_delivery": null,
      "budget_history": [],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": false
    },
    {
      "id": "SIM-APA-004",
      "kind": "layaway",
      "status": "settled",
      "branch": 1,
      "customer": {
        "name": "Cliente de prueba 04",
        "phone": "000 000 0004"
      },
      "created": "2026-07-28T12:00:00-06:00",
      "term": 45,
      "due": "2026-09-11",
      "ready": null,
      "total": 180000,
      "items": [
        {
          "name": "Anillo artesanal de muestra",
          "qty": 1,
          "price": 180000,
          "cost": 90000
        }
      ],
      "payments": [
        {
          "id": "SIM-APA-004-ANT",
          "kind": "Anticipo",
          "amount": 72000,
          "at": "2026-07-28T12:00:00-06:00",
          "branch": 1,
          "actor": "Melissa",
          "method": "Efectivo"
        },
        {
          "id": "SIM-APA-004-LIQ",
          "kind": "Liquidación",
          "amount": 108000,
          "at": "2026-09-06T12:00:00-06:00",
          "branch": 2,
          "actor": "Ximena",
          "method": "Tarjeta · Banco de prueba · 1234"
        }
      ],
      "history": [
        {
          "at": "2026-07-28T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Registrado",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-06T12:00:00-06:00",
          "actor": "Ximena",
          "from": "Pendiente de pago",
          "to": "Liquidación",
          "note": "Cobro de ejemplo en sucursal 2"
        }
      ],
      "delivery": null,
      "settled": "2026-09-06T12:00:00-06:00",
      "sellers": [
        "Melissa",
        "Jessica"
      ],
      "work": "",
      "expected_delivery": null,
      "budget_history": [],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": false
    },
    {
      "id": "SIM-APA-005",
      "kind": "layaway",
      "status": "delivered",
      "branch": 2,
      "customer": {
        "name": "Cliente de prueba 05",
        "phone": "000 000 0005"
      },
      "created": "2026-09-17T12:00:00-06:00",
      "term": 45,
      "due": "2026-11-01",
      "ready": null,
      "total": 120000,
      "items": [
        {
          "name": "Anillo artesanal de muestra",
          "qty": 1,
          "price": 120000,
          "cost": 60000
        }
      ],
      "payments": [
        {
          "id": "SIM-APA-005-ANT",
          "kind": "Anticipo",
          "amount": 48000,
          "at": "2026-09-17T12:00:00-06:00",
          "branch": 2,
          "actor": "Melissa",
          "method": "Efectivo"
        },
        {
          "id": "SIM-APA-005-LIQ",
          "kind": "Liquidación",
          "amount": 72000,
          "at": "2026-09-24T12:00:00-06:00",
          "branch": 1,
          "actor": "Ximena",
          "method": "Tarjeta · Banco de prueba · 1234"
        }
      ],
      "history": [
        {
          "at": "2026-09-17T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Registrado",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-24T12:00:00-06:00",
          "actor": "Ximena",
          "from": "Pendiente de pago",
          "to": "Liquidación",
          "note": "Cobro de ejemplo en sucursal 1"
        },
        {
          "at": "2026-09-25T17:00:00-06:00",
          "actor": "Citlali",
          "from": "Liquidado pendiente de entrega",
          "to": "Entregado",
          "note": "Conjunto completo entregado desde POS."
        }
      ],
      "delivery": {
        "at": "2026-09-25T17:00:00-06:00",
        "branch": 1,
        "actor": "Citlali",
        "receipt": "SIM-APA-005-ENT",
        "signature": false
      },
      "settled": "2026-09-24T12:00:00-06:00",
      "sellers": [
        "Melissa",
        "Jessica"
      ],
      "work": "",
      "expected_delivery": null,
      "budget_history": [],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": false
    },
    {
      "id": "SIM-APA-006",
      "kind": "layaway",
      "status": "cancelled",
      "branch": 1,
      "customer": {
        "name": "Cliente de prueba 06",
        "phone": "000 000 0006"
      },
      "created": "2026-09-21T12:00:00-06:00",
      "term": 45,
      "due": "2026-11-05",
      "ready": null,
      "total": 100000,
      "items": [
        {
          "name": "Anillo artesanal de muestra",
          "qty": 1,
          "price": 100000,
          "cost": 50000
        }
      ],
      "payments": [
        {
          "id": "SIM-APA-006-ANT",
          "kind": "Anticipo",
          "amount": 40000,
          "at": "2026-09-21T12:00:00-06:00",
          "branch": 1,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-09-21T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Registrado",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-23T12:00:00-06:00",
          "actor": "Carlo",
          "from": "Pendiente",
          "to": "Cancelado",
          "note": "Mercancía por 400.0 MXN a cambio del anticipo; sin diferencia ni devolución de efectivo. Se liberaron las piezas originales."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [
        "Melissa",
        "Jessica"
      ],
      "work": "",
      "expected_delivery": null,
      "budget_history": [],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": false
    },
    {
      "id": "SIM-APA-007",
      "kind": "layaway",
      "status": "released",
      "branch": 2,
      "customer": {
        "name": "Cliente de prueba 07",
        "phone": "000 000 0007"
      },
      "created": "2026-08-02T12:00:00-06:00",
      "term": 45,
      "due": "2026-09-16",
      "ready": null,
      "total": 90000,
      "items": [
        {
          "name": "Anillo artesanal de muestra",
          "qty": 1,
          "price": 90000,
          "cost": 45000
        }
      ],
      "payments": [
        {
          "id": "SIM-APA-007-ANT",
          "kind": "Anticipo",
          "amount": 36000,
          "at": "2026-08-02T12:00:00-06:00",
          "branch": 2,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-08-02T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Registrado",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-25T12:00:00-06:00",
          "actor": "Carlo",
          "from": "Pendiente",
          "to": "Liberado",
          "note": "Liberación autorizada tras vencer; pagos e historial conservados."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [
        "Melissa",
        "Jessica"
      ],
      "work": "",
      "expected_delivery": null,
      "budget_history": [],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": false
    },
    {
      "id": "SIM-REP-011",
      "kind": "repair",
      "status": "received",
      "branch": 2,
      "customer": {
        "name": "Cliente de prueba 11",
        "phone": "000 000 0011"
      },
      "created": "2026-09-24T12:00:00-06:00",
      "term": 45,
      "due": null,
      "ready": null,
      "total": 60000,
      "items": [
        {
          "name": "Anillo del cliente · aro abierto",
          "qty": 1
        },
        {
          "name": "Cadena del cliente · broche roto",
          "qty": 1
        }
      ],
      "payments": [
        {
          "id": "SIM-REP-011-ANT",
          "kind": "Anticipo",
          "amount": 30000,
          "at": "2026-09-24T12:00:00-06:00",
          "branch": 2,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-09-24T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Recibida",
          "note": "Recepción y anticipo de ejemplo."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [],
      "work": "Soldar aro y cambiar broche; revisar acabado sin modificar las piezas.",
      "expected_delivery": "2026-10-04",
      "budget_history": [
        {
          "at": "2026-09-24T12:00:00-06:00",
          "before": null,
          "after": 60000,
          "actor": "Melissa",
          "reason": "Presupuesto acordado al recibir.",
          "agreement": "Aceptación de ejemplo al recibir."
        }
      ],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": false
    },
    {
      "id": "SIM-REP-012",
      "kind": "repair",
      "status": "in_repair",
      "branch": 1,
      "customer": {
        "name": "Cliente de prueba 12",
        "phone": "000 000 0012"
      },
      "created": "2026-09-18T12:00:00-06:00",
      "term": 45,
      "due": null,
      "ready": null,
      "total": 80000,
      "items": [
        {
          "name": "Anillo del cliente · aro abierto",
          "qty": 1
        },
        {
          "name": "Cadena del cliente · broche roto",
          "qty": 1
        }
      ],
      "payments": [
        {
          "id": "SIM-REP-012-ANT",
          "kind": "Anticipo",
          "amount": 30000,
          "at": "2026-09-18T12:00:00-06:00",
          "branch": 1,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-09-18T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Recibida",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-19T12:00:00-06:00",
          "actor": "Carlo",
          "from": "Recibida",
          "to": "En reparación",
          "note": "Inicio del trabajo."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [],
      "work": "Soldar aro y cambiar broche; revisar acabado sin modificar las piezas.",
      "expected_delivery": "2026-09-28",
      "budget_history": [
        {
          "at": "2026-09-18T12:00:00-06:00",
          "before": null,
          "after": 60000,
          "actor": "Melissa",
          "reason": "Presupuesto acordado al recibir.",
          "agreement": "Aceptación de ejemplo al recibir."
        },
        {
          "at": "2026-09-20T12:00:00-06:00",
          "before": 60000,
          "after": 80000,
          "actor": "Carlo",
          "reason": "Trabajo adicional en el broche.",
          "agreement": "Aceptación del cliente simulada; formato definitivo pendiente."
        }
      ],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": true
    },
    {
      "id": "SIM-REP-013",
      "kind": "repair",
      "status": "ready",
      "branch": 2,
      "customer": {
        "name": "Cliente de prueba 13",
        "phone": "000 000 0013"
      },
      "created": "2026-09-14T12:00:00-06:00",
      "term": 45,
      "due": "2026-11-07",
      "ready": "2026-09-23T12:00:00-06:00",
      "total": 90000,
      "items": [
        {
          "name": "Anillo del cliente · aro abierto",
          "qty": 1
        },
        {
          "name": "Cadena del cliente · broche roto",
          "qty": 1
        }
      ],
      "payments": [
        {
          "id": "SIM-REP-013-ANT",
          "kind": "Anticipo",
          "amount": 45000,
          "at": "2026-09-14T12:00:00-06:00",
          "branch": 2,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-09-14T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Recibida",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-15T12:00:00-06:00",
          "actor": "Carlo",
          "from": "Recibida",
          "to": "En reparación",
          "note": "Inicio del trabajo."
        },
        {
          "at": "2026-09-23T12:00:00-06:00",
          "actor": "Carlo",
          "from": "En reparación",
          "to": "Lista para entregar",
          "note": "Comienza el plazo de recogida de 45 días naturales."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [],
      "work": "Soldar aro y cambiar broche; revisar acabado sin modificar las piezas.",
      "expected_delivery": "2026-09-24",
      "budget_history": [
        {
          "at": "2026-09-14T12:00:00-06:00",
          "before": null,
          "after": 90000,
          "actor": "Melissa",
          "reason": "Presupuesto acordado al recibir.",
          "agreement": "Aceptación de ejemplo al recibir."
        }
      ],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": true
    },
    {
      "id": "SIM-REP-014",
      "kind": "repair",
      "status": "ready",
      "branch": 1,
      "customer": {
        "name": "Cliente de prueba 14",
        "phone": "000 000 0014"
      },
      "created": "2026-07-18T12:00:00-06:00",
      "term": 45,
      "due": "2026-09-21",
      "ready": "2026-08-07T12:00:00-06:00",
      "total": 100000,
      "items": [
        {
          "name": "Anillo del cliente · aro abierto",
          "qty": 1
        },
        {
          "name": "Cadena del cliente · broche roto",
          "qty": 1
        }
      ],
      "payments": [
        {
          "id": "SIM-REP-014-ANT",
          "kind": "Anticipo",
          "amount": 50000,
          "at": "2026-07-18T12:00:00-06:00",
          "branch": 1,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-07-18T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Recibida",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-07-19T12:00:00-06:00",
          "actor": "Carlo",
          "from": "Recibida",
          "to": "En reparación",
          "note": "Inicio del trabajo."
        },
        {
          "at": "2026-08-07T12:00:00-06:00",
          "actor": "Carlo",
          "from": "En reparación",
          "to": "Lista para entregar",
          "note": "Comienza el plazo de recogida de 45 días naturales."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [],
      "work": "Soldar aro y cambiar broche; revisar acabado sin modificar las piezas.",
      "expected_delivery": "2026-07-28",
      "budget_history": [
        {
          "at": "2026-07-18T12:00:00-06:00",
          "before": null,
          "after": 100000,
          "actor": "Melissa",
          "reason": "Presupuesto acordado al recibir.",
          "agreement": "Aceptación de ejemplo al recibir."
        }
      ],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": true
    },
    {
      "id": "SIM-REP-015",
      "kind": "repair",
      "status": "delivered",
      "branch": 2,
      "customer": {
        "name": "Cliente de prueba 15",
        "phone": "000 000 0015"
      },
      "created": "2026-09-08T12:00:00-06:00",
      "term": 45,
      "due": "2026-11-05",
      "ready": "2026-09-21T12:00:00-06:00",
      "total": 70000,
      "items": [
        {
          "name": "Anillo del cliente · aro abierto",
          "qty": 1
        },
        {
          "name": "Cadena del cliente · broche roto",
          "qty": 1
        }
      ],
      "payments": [
        {
          "id": "SIM-REP-015-ANT",
          "kind": "Anticipo",
          "amount": 35000,
          "at": "2026-09-08T12:00:00-06:00",
          "branch": 2,
          "actor": "Melissa",
          "method": "Efectivo"
        },
        {
          "id": "SIM-REP-015-LIQ",
          "kind": "Liquidación",
          "amount": 35000,
          "at": "2026-09-24T12:00:00-06:00",
          "branch": 1,
          "actor": "Ximena",
          "method": "Tarjeta · Banco de prueba · 1234"
        }
      ],
      "history": [
        {
          "at": "2026-09-08T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Recibida",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-09T12:00:00-06:00",
          "actor": "Carlo",
          "from": "Recibida",
          "to": "En reparación",
          "note": "Inicio del trabajo."
        },
        {
          "at": "2026-09-21T12:00:00-06:00",
          "actor": "Carlo",
          "from": "En reparación",
          "to": "Lista para entregar",
          "note": "Comienza el plazo de recogida de 45 días naturales."
        },
        {
          "at": "2026-09-24T12:00:00-06:00",
          "actor": "Ximena",
          "from": "Pendiente de pago",
          "to": "Liquidación",
          "note": "Cobro de ejemplo en sucursal 1"
        },
        {
          "at": "2026-09-25T17:00:00-06:00",
          "actor": "Citlali",
          "from": "Lista para entregar",
          "to": "Entregado",
          "note": "Conjunto completo entregado desde POS."
        }
      ],
      "delivery": {
        "at": "2026-09-25T17:00:00-06:00",
        "branch": 1,
        "actor": "Citlali",
        "receipt": "SIM-REP-015-ENT",
        "signature": true
      },
      "settled": "2026-09-24T12:00:00-06:00",
      "sellers": [],
      "work": "Soldar aro y cambiar broche; revisar acabado sin modificar las piezas.",
      "expected_delivery": "2026-09-18",
      "budget_history": [
        {
          "at": "2026-09-08T12:00:00-06:00",
          "before": null,
          "after": 70000,
          "actor": "Melissa",
          "reason": "Presupuesto acordado al recibir.",
          "agreement": "Aceptación de ejemplo al recibir."
        }
      ],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": true
    },
    {
      "id": "SIM-REP-016",
      "kind": "repair",
      "status": "cancelled",
      "branch": 1,
      "customer": {
        "name": "Cliente de prueba 16",
        "phone": "000 000 0016"
      },
      "created": "2026-09-22T12:00:00-06:00",
      "term": 45,
      "due": null,
      "ready": null,
      "total": 60000,
      "items": [
        {
          "name": "Anillo del cliente · aro abierto",
          "qty": 1
        },
        {
          "name": "Cadena del cliente · broche roto",
          "qty": 1
        }
      ],
      "payments": [
        {
          "id": "SIM-REP-016-ANT",
          "kind": "Anticipo",
          "amount": 30000,
          "at": "2026-09-22T12:00:00-06:00",
          "branch": 1,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-09-22T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Recibida",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-24T12:00:00-06:00",
          "actor": "Carlo",
          "from": "Recibida",
          "to": "Cancelado",
          "note": "Mercancía por 300.0 MXN a cambio del anticipo; sin diferencia ni devolución de efectivo. Piezas del cliente devueltas; firma manuscrita de ejemplo."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [],
      "work": "Soldar aro y cambiar broche; revisar acabado sin modificar las piezas.",
      "expected_delivery": "2026-10-02",
      "budget_history": [
        {
          "at": "2026-09-22T12:00:00-06:00",
          "before": null,
          "after": 60000,
          "actor": "Melissa",
          "reason": "Presupuesto acordado al recibir.",
          "agreement": "Aceptación de ejemplo al recibir."
        }
      ],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": false
    },
    {
      "id": "SIM-REP-017",
      "kind": "repair",
      "status": "received",
      "branch": 2,
      "customer": {
        "name": "Cliente de prueba 17",
        "phone": "000 000 0017"
      },
      "created": "2026-09-17T12:00:00-06:00",
      "term": 45,
      "due": null,
      "ready": null,
      "total": 50000,
      "items": [
        {
          "name": "Anillo del cliente · aro abierto",
          "qty": 1
        },
        {
          "name": "Cadena del cliente · broche roto",
          "qty": 1
        }
      ],
      "payments": [
        {
          "id": "SIM-REP-017-ANT",
          "kind": "Anticipo",
          "amount": 25000,
          "at": "2026-09-17T12:00:00-06:00",
          "branch": 2,
          "actor": "Melissa",
          "method": "Efectivo"
        }
      ],
      "history": [
        {
          "at": "2026-09-17T12:00:00-06:00",
          "actor": "Melissa",
          "from": "—",
          "to": "Recibida",
          "note": "Recepción y anticipo de ejemplo."
        },
        {
          "at": "2026-09-18T12:00:00-06:00",
          "actor": "Carlo",
          "from": "Recibida",
          "to": "En reparación",
          "note": "Inicio registrado."
        },
        {
          "at": "2026-09-19T12:00:00-06:00",
          "actor": "Carlo",
          "from": "En reparación",
          "to": "Recibida",
          "note": "Corrección con motivo: estado capturado por error. La cancelación sigue bloqueada."
        }
      ],
      "delivery": null,
      "settled": null,
      "sellers": [],
      "work": "Soldar aro y cambiar broche; revisar acabado sin modificar las piezas.",
      "expected_delivery": "2026-09-27",
      "budget_history": [
        {
          "at": "2026-09-17T12:00:00-06:00",
          "before": null,
          "after": 50000,
          "actor": "Melissa",
          "reason": "Presupuesto acordado al recibir.",
          "agreement": "Aceptación de ejemplo al recibir."
        }
      ],
      "notes": "Datos completamente ficticios para revisar pantallas. El teléfono no es un contacto real.",
      "ever_in_repair": true
    }
  ]
};
if(typeof module!=='undefined')module.exports=ORDER_DEMO;
