import os

def filter_YOLO(yolo_dir, export_dir, ids):
    ext = 'txt'

    print("searching for annotations files with .txt extension")
    txtFiles = [ files for files in os.listdir(import_dir) if files.endswith(ext) ]

    print('filtering ...')
    for gtFile in txtFiles:
        gtFilePath = yolo_dir + '/' + gtFile
        saveFilePath = export_dir + '/' + gtFile
        with open(gtFilePath, 'r') as f:
            lines = f.read().splitlines()

        del_index = []
        with open(saveFilePath, 'w') as f:
            print(saveFilePath)
            for i in range(len(lines)):
                if lines[i][0] not in ids:
                    del_index.append(i)

            for index in sorted(del_index, reverse=True):
                del lines[index]
            ids.sort()
            for i in range(len(lines)):
                idx = ids.index(lines[i][0])
                list_lines = list(lines[i])
                list_lines[0] = str(idx)
                lines[i] = ''.join(list_lines)

            for line in lines:
                f.write(f"{line}\n")
    print("Done! Files stored in " + os.getcwd() + '/' + export_dir)

def remove_labels(image_dir, label_dir, del_ids):
    ext = 'txt'

    print("searching for annotations files with .txt extension")
    txtFiles = [ files for files in os.listdir(label_dir) if files.endswith(ext) ]

    print('filtering ...')

    del_file = []
    for gtFile in txtFiles:
        gtFilePath = label_dir + '/' + gtFile
        with open(gtFilePath, 'r') as f:
            lines = f.read().splitlines()

            for i in range(len(lines)):
                if lines[i][0] in del_ids:
                    del_file.append(os.path.splitext(gtFile)[0])
                    break
    print("delete list: ", del_file)
    for file in del_file:
        os.remove(label_dir + '/' + file + '.txt')
        os.remove(image_dir + '/' + file + '.jpg')

def change_id(label_import, label_export, old_id, new_id):
    ext = 'txt'

    print("searching for annotations files with .txt extension")
    txtFiles = [ files for files in os.listdir(label_import) if files.endswith(ext) ]

    print('changing ID ...')

    for gtFile in txtFiles:
        gtFilePath = label_import + '/' + gtFile
        saveFilePath = label_export + '/' + gtFile
        with open(gtFilePath, 'r') as f:
            lines = f.read().splitlines()

        with open(saveFilePath, 'w') as f:
            print(saveFilePath)
            for i in range(len(lines)):
                if lines[i][0]==old_id:
                    list_lines = list(lines[i])
                    list_lines[0] = str(new_id)
                    lines[i] = ''.join(list_lines)

            
            for line in lines:
                f.write(f"{line}\n")

def count_class(annotation_dir):
    class_instances = {}
    ext = 'txt'

    print("searching for annotations files with .txt extension")
    txtFiles = [ files for files in os.listdir(annotation_dir) if files.endswith(ext) ]

    print('counting class instances ...')

    for gtFile in txtFiles:
        gtFilePath = annotation_dir + '/' + gtFile
        with open(gtFilePath, 'r') as f:
            lines = f.read().splitlines()
            for i in range(len(lines)):
                line = lines[i].split(" ")
                if line[0] not in class_instances:
                    class_instances[str(line[0])] = 1
                else:
                    class_instances[str(line[0])] += 1
    
    print('Number of class instances are as follows : ', class_instances)


if __name__ == "__main__":
    # flag value determines run-time functionality. 0: Filter class IDs, 1: Removing the label and image files of specified class IDs, 2: To change ID from one value to another, 3: to count the number of instances of each class.
    flag = int(input("Enter 0 for filtering classes, 1 for removing labels and images with specific class IDs, 2 for changing class ID, 3 for counting the number of instances of each class: "))

    if flag == 0:
        # Filters the class
        import_dir = input("Enter the name of import directory for the annotations to be filtered (should be present in the root directory): ")
        if not os.path.exists(os.getcwd() + "/" + import_dir):
            print("Directory does not exist! Enter a valid label directory present in the root.")

        save_dir = input("Enter the name of save directory for the filtered annotations (should be present in the root directory): ")
        if not os.path.exists(os.getcwd() + "/" + save_dir):
            print("Directory does not exist! Making a new directory for export ...")
            os.makedirs(os.getcwd() + "/" + save_dir)

        filter_IDs = input("Enter class IDs to retain with comma seperation: ").split(",")

        filter_YOLO(import_dir, save_dir, filter_IDs)
    
    elif flag == 1:
        # Removes specified class IDs labels and image files
        labels = input("Enter the name of directory with labels (should be present in the root directory): ")
        if not os.path.exists(os.getcwd() + "/" + labels):
            print("Directory does not exist! Enter a valid label directory present in the root.")
            exit()

        images = input("Enter the name of directory with images (should be present in the root directory): ")
        if not os.path.exists(os.getcwd() + "/" + images):
            print("Directory does not exist! Enter a valid image directory present in the root.")
            exit()

        del_IDs = input("Enter class IDs to delete with comma seperation: ").split(",")

        remove_labels(images, labels, del_IDs)

    elif flag == 2:
        # Changing class ID from one to another
        import_dir = input("Enter the name of import directory for the annotations to be filtered (should be present in the root directory): ")
        if not os.path.exists(os.getcwd() + "/" + import_dir):
            print("Directory does not exist! Enter a valid label directory present in the root.")

        save_dir = input("Enter the name of save directory for the filtered annotations (should be present in the root directory): ")
        if not os.path.exists(os.getcwd() + "/" + save_dir):
            print("Directory does not exist! Making a new directory for export ...")
            os.makedirs(os.getcwd() + "/" + save_dir)

        prev_id, mod_id = input("Enter old class ID and new class ID with comma seperation: ").split(",")

        change_id(import_dir, save_dir, prev_id, mod_id)

    elif flag == 3:
        # Count instances of each class in the dataset
        label_dir = input('Enter name of the directory with all the YOLO label files: ')
        if not os.path.exists(os.getcwd() + "/" + label_dir):
            print("Directory does not exist! Enter a valid label directory present in the root.")
        # num_classes = input("Enter number of classes in the dataset")
        count_class(label_dir)
