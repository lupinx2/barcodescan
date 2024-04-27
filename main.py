import PySimpleGUI as sg
import json

# Define the layout of the window
text_capture = sg.Text("", size=(16, 1))
table_data = []

layout = [
    [sg.Text("Punto De Venta")],
    [text_capture],
    [sg.Table(table_data, headings=["Producto", "Precio", "Cantidad", "Total"], key="-TABLE-")],
    [sg.Text("Total: $0.00", key="-TOTAL-")],   
    [sg.Button("Salir"), sg.Button("Reset", button_color="red"), sg.Button("Finalizar Compra", button_color="green")]
]

# Create the window
window = sg.Window("Generic Window", layout, use_default_focus=False, return_keyboard_events=True)

def code_to_product(code):
    with open("products.json") as file:
        data = json.load(file)
        products = data["products"]
        for product in products:
            if product["productID"] == code:
                product_info = [product["name"],product["price"], 1]
                return product_info
    return None

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Salir":
        break

    if event == "Reset":
        text_capture.update("")
        table_data = []
        window["-TABLE-"].update(values=table_data)
        window["-TOTAL-"].update("Total: $0.00")
        continue

    if event == "Finalizar Compra":
        continue

    if event.find("MouseWheel") == 0 or event.find("Shift_") == 0 or event.find("Control_") == 0 or event.find("Alt_") == 0 or event.find("Tab") == 0:
        event = ""
        continue

    if event == "Return:36":
        scanned_code = text_capture.get()
        text_capture.update("")
        product_info = code_to_product(scanned_code)
        if product_info == None:
            text_capture.update("Codigo no encontrado")
            continue
        table_data = window["-TABLE-"].get()
        table_data.append([product_info[0], product_info[1], 1, product_info[1]])
        window["-TABLE-"].update(values=table_data)
        print("Row added")
        continue
    else:
        text_capture.update( text_capture.get() + event[0])
        print(event)
        continue
    

# Close the window
window.close()