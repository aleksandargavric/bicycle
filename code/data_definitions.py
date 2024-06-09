input_csv_file = 'testdata.csv'

# Activities for domain 1 (DNA)
activitiesD1ext = ['no action', 'unboxing', 'filling tube by spitting', 'replacing caps', 'shaking tube', 'checking tube', 'placing tube into biohazard bag', 'sealing biohazard bag', 'reading printed user manual', 'reading web user manual', 'cleaning the space', 'packing the mail', 'filling up a form', 'typing data entry', 'activating test kit online', 'placing sample container in provided packaging', 'sealing outer packaging']
activitiesD1red  = ['unboxing', 'filling tube by spitting', 'replacing caps', 'shaking tube', 'checking tube', 'sealing biohazard bag', 'placing tube into biohazard bag']

# Activities for domain 2 (IKEA)
activitiesD2 = ['no action', 'unboxing', 'drilling', 'aligning parts', 'reading printed user manual', 'screwing', 'fitting components together', 'tightening bolts and screws', 'attaching hardware', 'adjusting hinges and sliders', 'securing joints', 'assembling drawers and shelves', 'installing legs or wheels', 'mounting brackets', 'positioning back panels', 'fastening dowels', 'testing stability and functionality']

# Input data values
vision_values = [
        {"start": 2400, "end": 2450, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2450, "end": 2500, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2500, "end": 2550, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2550, "end": 2600, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2600, "end": 2650, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2650, "end": 2700, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2700, "end": 2750, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2750, "end": 2800, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2800, "end": 2850, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2850, "end": 2900, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2900, "end": 2950, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2950, "end": 3000, "domain": activitiesD2, "data": input_csv_file},
        {"start": 3000, "end": 3050, "domain": activitiesD2, "data": input_csv_file},
        {"start": 3050, "end": 3100, "domain": activitiesD2, "data": input_csv_file},
        {"start": 3100, "end": 3150, "domain": activitiesD2, "data": input_csv_file},
        {"start": 3150, "end": 3200, "domain": activitiesD2, "data": input_csv_file},
        {"start": 3200, "end": 3247, "domain": activitiesD2, "data": input_csv_file},
        {"start": 776, "end": 800, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 800, "end": 850, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 850, "end": 900, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 900, "end": 950, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 950, "end": 1000, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1000, "end": 1050, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1050, "end": 1100, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1100, "end": 1150, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1150, "end": 1200, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1200, "end": 1225, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1225, "end": 1250, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1250, "end": 1300, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1300, "end": 1350, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1350, "end": 1400, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1400, "end": 1450, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1450, "end": 1500, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 1500, "end": 1551, "domain": activitiesD1ext, "data": input_csv_file}
    ]

audio_values = [
        {"start": 1552, "end": 1600, "domain": activitiesD2, "data": input_csv_file},
        {"start": 1600, "end": 1650, "domain": activitiesD2, "data": input_csv_file},
        {"start": 1650, "end": 1700, "domain": activitiesD2, "data": input_csv_file},
        {"start": 1700, "end": 1750, "domain": activitiesD2, "data": input_csv_file},
        {"start": 1750, "end": 1800, "domain": activitiesD2, "data": input_csv_file},
        {"start": 1800, "end": 1850, "domain": activitiesD2, "data": input_csv_file},
        {"start": 1850, "end": 1900, "domain": activitiesD2, "data": input_csv_file},
        {"start": 1900, "end": 1950, "domain": activitiesD2, "data": input_csv_file},
        {"start": 1950, "end": 2000, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2000, "end": 2050, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2050, "end": 2100, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2100, "end": 2150, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2150, "end": 2200, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2200, "end": 2250, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2250, "end": 2300, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2300, "end": 2350, "domain": activitiesD2, "data": input_csv_file},
        {"start": 2350, "end": 2399, "domain": activitiesD2, "data": input_csv_file},
        {"start": 0, "end": 50, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 50, "end": 100, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 100, "end": 150, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 150, "end": 200, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 200, "end": 250, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 250, "end": 300, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 300, "end": 327, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 327, "end": 350, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 350, "end": 400, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 400, "end": 450, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 450, "end": 500, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 500, "end": 550, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 550, "end": 600, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 600, "end": 650, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 650, "end": 700, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 700, "end": 750, "domain": activitiesD1ext, "data": input_csv_file},
        {"start": 750, "end": 775, "domain": activitiesD1ext, "data": input_csv_file}
    ]

vision_values_reduced = [
        {"start": 776, "end": 800, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 800, "end": 850, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 850, "end": 900, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 900, "end": 950, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 950, "end": 1000, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1000, "end": 1050, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1050, "end": 1100, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1100, "end": 1150, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1150, "end": 1200, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1200, "end": 1225, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1225, "end": 1250, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1250, "end": 1300, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1300, "end": 1350, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1350, "end": 1400, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1400, "end": 1450, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1450, "end": 1500, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 1500, "end": 1551, "domain": activitiesD1red, "data": input_csv_file}
    ]

audio_values_reduced = [
        {"start": 0, "end": 50, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 50, "end": 100, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 100, "end": 150, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 150, "end": 200, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 200, "end": 250, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 250, "end": 300, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 300, "end": 327, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 327, "end": 350, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 350, "end": 400, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 400, "end": 450, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 450, "end": 500, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 500, "end": 550, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 550, "end": 600, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 600, "end": 650, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 650, "end": 700, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 700, "end": 750, "domain": activitiesD1red, "data": input_csv_file},
        {"start": 750, "end": 775, "domain": activitiesD1red, "data": input_csv_file},
    ]
