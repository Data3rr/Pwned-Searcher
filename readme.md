![logo](https://i.postimg.cc/HsbffSqw/Screenshot-2024-05-13-213529.png)

# Pwned searcher

Pwned searcher is a local website that allows you to search databases quickly and easily using Apache Solr.

# Features 
- Search by term *(username, email, ip...)*
- Supports large amounts of data *(millions of data records)*
- Parser with 9 integrated schemas
- Cusotomizable *(requires basic knowledge of Python, Html and Solr)*

# Requirements 
- **Windows 10/11** OS only *(win32, for x86, x86_64, and arm64 architectures)*
- **Python 3.x** *(python 3.10 used for the project.)*
- **Java installed** *(JAVA_HOME environment variable configured)*
- **Modules:** *(colorama)*

# Usage 
### 1. First step - Checkup
- Check that you have installed the modules. If not, run the following command in the pwned directory: `pip install -r requirements.txt`
- Check that you have Java installed on your PC, otherwise download it [here](https://www.java.com/download/ie_manual.jsp)
- Check that you've defined the JAVA_HOME environment variable correctly, if not find the solution [here](https://stackoverflow.com/questions/11161248/setting-java-home)

### 2. Second step - Startup
- Install Pwned by running the command `python Pwned_installer.py` and select your installation directory
- Now you can directly execute the command `python Pwned_searcher.py` to get started
- Once the program has run without errors, you need to define the allocated ram by going to menu 2 by pressing 2, then enter the amount of ram in **GO**. *(it will be saved)*
- Now use the Start menu by pressing 1 to start running Solr and the local web server.
- Maintenant vous pouvez accéder directement à l'interface de recherche grace au lien `localhost:5000`

### 3. Third step - Import data
- To import data you can use the built-in parser in the `parser` folder.
- To use it, you need to follow the instructions it gives you, bearing in mind that the default Solr core name is `searcher`. You must give it only txt files respecting the supported schemas *(Warning! explored files and folders must not contain spaces)*.

- If you want to import your own data, you can use the post.jar in the parser folder, but please note that the data must be organized as Solr requires. Also, if you want to add fields not present in the basic Pwned version, they must be filled in the Solr panel `localhost:8983` - > `Core selector` -> `searcher` -> `Schema` -> create your schema (mytypeoffield) the type to be filled in will be `string`. For more information, please refer to the [Solr offical documentation](https://solr.apache.org/guide/8_8/post-tool.html). 

# Disclaimer 
This website developed by Adapters, enables you to search databases quickly using Apache Solr, it is intended for **EDUCATIONAL PURPOSES ONLY**, to help you learn how to manipulate your **own** databases an search into your **own** databases, for example. **Under no circumstances should it be used for malicious purposes.**

# Credits
- This project was created by Adapters using Apache Solr, and you can find their official website [here](https://solr.apache.org/).
