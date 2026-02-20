from wikipedia_scraper import update_leaders_data, export_to_json, save_to_csv



if __name__ == "__main__":
    print("Updating leaders data...This may take some time")
    update_leaders_data()
    
    print("Exporting data to json file...")
    export_to_json("leaders.json")
    
    print("Your 'leaders.json' file was created succesfully...")
    
    print("Saving data into CSV...")
    save_to_csv("leaders.csv")