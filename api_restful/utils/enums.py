import enum

class OrderStatus(enum.Enum):
    created = "created"         # Assim que o pedido é feito
    processing = "processing"   # Quando está sendo separado ou montado
    completed = "completed"     # Quando o pedido foi entregue/concluído
    canceled = "canceled"       # Se o pedido for cancelado

class GenderStatus(enum.Enum):
    female = 0
    male = 1
    other = 2    