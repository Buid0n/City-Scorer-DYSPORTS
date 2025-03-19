from customtkinter import *
from PIL import Image
import json

app = CTk()
app.geometry("500x400")

set_appearance_mode("dark")

# Open data
with open('Facilities.json', 'r') as file: 
    data = json.load(file)

with open('us-cities-table.json','r') as file: 
    cities = json.load(file)
    options = [f"{city['city']}, {city['state']}" for city in cities[:350]]
    
# number of basketball facilities - calculated based on cities with largest number of basketball hoops per 10000 residents in the US (2023)
city_hoops = {}
for entry in data[2:]:
    city = entry.get("Cities with the most public basketball hoops per 10,000 residents in the U.S. 2023", "").strip()
    hoops = entry.get("","")
    if city and hoops:
        city_hoops[city] = hoops

# Supporting Functions
def show(): # Show Population
    selected_city = combobox.get()
    for city in cities: 
        if f"{city['city']}, {city['state']}" == selected_city:
            label.configure(text = f"Population: {city['pop2024']}")
            return
        
def show_hoops():
    selected_city = combobox.get().split(",")[0] # extract only city name
    hoops = city_hoops.get(selected_city, "Data Unavailable")
    hoops_label.configure(text = f"Public Hoops: {hoops} per 10K residents")
        
def score_city():
     # Get selected city
    selected_city = combobox.get()
    Population = None

    for city in cities:
        if f"{city['city']}, {city['state']}" == selected_city:
            Population = city['pop2024']
            break

    if Population is None:
        print("Error: Please select a valid city.")
        return
    
    # variables to consider - Upper bounds
    Pop_ub = 759915
    Income_ub = 123000
    Hs_ub = 21
    Ms_ub = 23
    Es_ub = 77

    # variables to consider - Lower bounds
    Pop_lb = 178056
    Income_lb = 89619
    Hs_lb = 7
    Ms_lb = 7
    Es_lb = 22

    try:
        Income = int(Income_entry.get()) if Income_entry.get().strip() else Income_lb
        Hs = int(Hs_entry.get()) if Hs_entry.get().strip() else Hs_lb
        Ms = int(Ms_entry.get()) if Ms_entry.get().strip() else Ms_lb
        Es = int(Es_entry.get()) if Es_entry.get().strip() else Es_lb
    except ValueError:
        print("Error: Please enter valid numerical values.")
        return

    pop_score = 1 + 9 * (Population - Pop_lb) / (Pop_ub - Pop_lb)
    income_score = 1 + 9 * (Income - Income_lb) / (Income_ub - Income_lb)
    hs_score = 1 + 9 * (Hs - Hs_lb) / (Hs_ub - Hs_lb)
    ms_score = 1 + 9 * (Ms - Ms_lb) / (Ms_ub - Ms_lb)
    es_score = 1 + 9 * (Es - Es_lb) / (Es_ub - Es_lb)

    score = round(pop_score * 0.2 + income_score * 0.2 + hs_score * .15 + ms_score * .15 + es_score * .15, 2)

    if 0.00 < score < 2.99: 
        message = "Not suitable, Poor alignment with business needs."
    elif 3.00 < score < 4.99: 
        message = "Low fit, may present challenges in key areas"
    elif 5.00 < score < 6.99:
        message = "Modearte fit, some good qualities but a few weaknesses to consider"
    elif 7.00 < score < 8.99:
        message = "Very good fit, high potential with strong infastructure and demographics"
    else: 
        message = "Excellent fit, ideal city for expansion, strong in all key metrics"

    Score_label.configure(text=f"Score: {score}\n{message}")

# Frames
frame = CTkScrollableFrame(master = app, fg_color = "#8D6F3A", border_color = "#FFCC70", border_width = 2, orientation = "vertical", width = 400)
frame.pack(expand = True)

# Labels
label = CTkLabel(master = frame, text = "Score a city!", font = ("Roboto", 16))
label.pack(expand = True, anchor = "n", padx = 10, pady = 30)

# Combobox
combobox = CTkComboBox(master = frame, values = options, fg_color = "#808080", 
                       border_color = "#808080", dropdown_fg_color = "#0093E9")

combobox.pack(expand = True, anchor = "center")

label = CTkLabel(master = frame, text = "" , font = ("Roboto", 12))
label.pack(expand = True, anchor = "n")

# Button
img = Image.open("population.png")

btn = CTkButton(master = frame, text = "Show Population", corner_radius = 32, fg_color = "#808080", 
                hover_color = "#4158D0", border_color = "#000000",
                border_width = 2, image = CTkImage(dark_image = img, light_image = img), command = show)

btn.pack(expand = True, anchor = "s", padx = 10, pady = 5)    

hoops_btn = CTkButton(master = frame, text = "Show Hoops Data", command = show_hoops)
hoops_btn.pack(expand = True, anchor = "s", padx = 10, pady = 5)

hoops_label = CTkLabel(master = frame, text = "", font = ("Roboto", 12))
hoops_label.pack(expand = True, anchor = "s", padx = 10, pady = 10)

# Entry Boxes
Income_entry = CTkEntry(master = frame, placeholder_text="Median Household Income ", width = 200)
Income_entry.pack(anchor = "s", expand = True, padx = 10, pady = 15)

Hs_entry = CTkEntry(master = frame, placeholder_text="Number of High Schools ", width = 200)
Hs_entry.pack(anchor = "s", expand = True, padx = 10, pady = 15)

Ms_entry = CTkEntry(master = frame, placeholder_text="Number of Middle Schools", width = 200)
Ms_entry.pack(anchor = "s", expand = True, padx = 10, pady = 15)

Es_entry = CTkEntry(master = frame, placeholder_text="Number of Elementary Schools", width = 200)
Es_entry.pack(anchor = "s", expand = True, padx = 10, pady = 20)


# Scoring button
Button = CTkButton(master = frame, text = "Score city", command = score_city)
Button.pack(expand = True, anchor = "s", padx = 10, pady = 5)
    
# Score Label
Score_label = CTkLabel(master = frame, text = "", font = ("Roboto", 12))
Score_label.pack(expand = True, anchor = "s", padx = 10, pady = 10)

# main
def main():
    app.mainloop()

if __name__ == "__main__": 
    main()