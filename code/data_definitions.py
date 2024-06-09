input_csv_file = 'testdata.csv'

# Activities for domain 1 (DNA)
activitiesD1ext = ['no action', 'unboxing', 'filling tube by spitting', 'replacing caps', 'shaking tube', 'checking tube', 'placing tube into biohazard bag', 'sealing biohazard bag', 'reading printed user manual', 'reading web user manual', 'cleaning the space', 'packing the mail', 'filling up a form', 'typing data entry', 'activating test kit online', 'placing sample container in provided packaging', 'sealing outer packaging']
activitiesD1red  = ['unboxing', 'filling tube by spitting', 'replacing caps', 'shaking tube', 'checking tube', 'sealing biohazard bag', 'placing tube into biohazard bag']

# Input data values
vision_values = [
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
