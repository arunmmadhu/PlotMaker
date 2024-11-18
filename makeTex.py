import os
import argparse
from collections import defaultdict

def generate_tex(image_dict, output_file="auto_plots.tex"):
    with open(output_file, "w") as tex_file:
        
        # Iterate through the folders in the specified order
        for superfolder, subfolders in image_dict.items():
            tex_file.write("\\section{{{0} Plots}}\n\n".format(os.path.basename(superfolder).replace("_", "\\_")))
            
            for subfolder, images in subfolders.items():
                section_name = os.path.basename(subfolder)
                tex_file.write("\\subsection{{{} Category}}\n".format(section_name))
                tex_file.write("\\label{{sec:{0}{1}}}\n\n".format(os.path.basename(superfolder).replace("_", ""),section_name))
                tex_file.write("\\begin{figure}[H]\n")
                tex_file.write("    \\centering\n")

                for idx, img_path in enumerate(images):
                    tex_file.write("    \\begin{subfigure}{0.2\\textwidth}\n")
                    tex_file.write("        \\includegraphics[width=\\textwidth]{{{}}}\n".format(img_path))
                    #tex_file.write("        \\caption{{{}}}\n".format(idx))
                    tex_file.write("        \\caption{{{}}}\n".format(""))
                    tex_file.write("    \\end{subfigure}\n")

                tex_file.write("    \\caption{{Triplet mass fits for {} category.}}\n".format(section_name))
                tex_file.write("    \\label{{fig:{0}{1}}}\n".format(os.path.basename(superfolder).replace("_", ""),section_name))
                tex_file.write("\\end{figure}\n\n")
        
        


def find_images_in_ultimate_subfolders(folders):
    organized_dict = defaultdict(lambda: defaultdict(list))  # Nested dictionary to group by superfolder and subfolder

    for root_folder in folders:
        if not os.path.isdir(root_folder):
            print("Warning: {} is not a valid directory. Skipping...".format(root_folder))
            continue
        for dirpath, dirnames, filenames in os.walk(root_folder):
            # If there are no subdirectories, it's an ultimate subfolder
            if not dirnames:
                images = [
                    os.path.join(dirpath, f)
                    for f in filenames
                    if f.lower().endswith(('.png', '.jpg'))
                ]
                if images:  # If there are images in this subfolder
                    superfolder = os.path.dirname(root_folder)
                    organized_dict[superfolder][dirpath].extend(images)

    return organized_dict

def main():
    parser = argparse.ArgumentParser(description="Find images in ultimate subfolders.")
    parser.add_argument(
        "-f", 
        "--folders", 
        nargs="+", 
        required=True, 
        help="List of root folders to search for images"
    )
    args = parser.parse_args()

    folders = args.folders
    image_dict = find_images_in_ultimate_subfolders(folders)

    # Generate the LaTeX file
    generate_tex(image_dict, output_file="auto_plots.tex")
    print("LaTeX file 'auto_plots.tex' generated successfully.")

if __name__ == "__main__":
    main()
