Guardicore Centra API - Label with dynamic criteria script
v1.0 | 2023-07-07
See 'changelog.txt' for full version history notes

=== How to use ===
1. Open the 'sample_creds.json' file and fill in your own API-privileged username and password combination.

2. Save as 'creds.json' in a secure location.

3. Open and edit the 'sample_dyn_criteria.txt' file

4. Add and edit any dynamic criteria you need. The script uses subnets as dynamic criteria by default, but you can
   change it to be hostnames or any other criteria you need. Follow the Centra API documentation for instructions and
   syntax.

5. Open the 'dynamic_label.py' file in a text editor, preferable Visual Studio Code or PyCharm.

6. Edit lines 10 and 11 to reflect your local machine file structure/directory and your unique Centra URL, respectively

7. When ready to run, open Powershell, bash, or a terminal and navigate to the file directory where the
   'dynamic_label.py' file is located.

8. Run the python file. For windows, this will be "python <python_file>.py".
   For MacOS/Linux, it will be ""./<python_file>.py". Don't forget to change the privileges on the python file to allow
   it to run.
