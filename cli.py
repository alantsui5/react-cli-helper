import sh
import inquirer
import os

class Reducer():
    def __init__(self):
        #Body of constructor
        print('inited')
    @staticmethod
    def determineUI(ui: str):
        if ui == 'zeit ui':
            addResult = sh.yarn('add', '@geist-ui/react')
            return 'zeit ui'
        elif ui == 'material ui':
            print('Enter Material UI')
            addResult = sh.yarn('add', '@material-ui/core')
            return 'material ui'
        elif ui == 'react bootstrap':
            print('Enter Bootstrap UI')
            addResult = sh.yarn('add', 'react-bootstrap', 'bootstrap')
            return 'react bootstrap'

    @staticmethod 
    def determineForm(form: str):
        if form == 'react hook form':
            addResult = sh.yarn('add', 'react-hook-form')
            return 'react hook form'
        elif form == 'formik':
            print('Enter formik')
            addResult = sh.yarn('add', 'formik')
            return 'formik'

    @staticmethod
    def determineGenerate(generator: str, name: str):
        if generator == 'component':
            tsx = Generator.generateTSX(name)
            return 'component'
        elif generator == 'page':
            tsx = Generator.generatePage(name)
            return 'page'
        elif generator == 'hook':
            tsx = Generator.generateHook(name)
            return 'hook'
        elif generator == 'global hook':
            tsx = Generator.generateGlobalHook(name)
            return 'global hook'

class Generator():
    @staticmethod
    def generateTSX(name: str):
        if name == '':
            return ''
        tsx = f"""import React from 'react'
        export function {name}(){{
            return <h1>Component {name}</h1>
        }}
        """
        Generator.generateFile(f'src/components/{name}.tsx', tsx)
        return tsx
    @staticmethod # this test is harder to write
    def generateFile(path: str, content: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as tsxFile:
            tsxFile.write(content)

    @staticmethod
    def generatePage(name: str):
        if name == '':
            return ''
        tsx = f"""import React from 'react'
        export function {name}(){{
            return <h1>Page {name}</h1>
        }}
        """
        Generator.generateFile(f'src/pages/{name}.tsx', tsx)
        return tsx

    @staticmethod
    def generateHook(name: str):
        if name == '':
            return ''
        hook = f"""import {{useState, useEffect}} from 'react'
        export function {name}(){{
            const [age, setAge] = useState<number>()
            const [name, setName] = useState<string>()
            return {{age, setAge, name, setName}}
        }}
        """
        print('The Hook is ')
        print(hook)
        Generator.generateFile(f'src/store/{name}.tsx', hook)
        return hook
    @staticmethod
    def generateGlobalHook(hookName: str):
        Generator.localHook(hookName)
        Transpiler.registerGlobalHook(hookName)
        return 'generate global hook'
    @staticmethod
    def generateStyle(style: bool, name: str):
        if style == True:
            style = ""
            Generator.generateFile(f'src/styles/{name}.module.sass', style)

class Transpiler():
    @staticmethod
    def registerGlobalHook(hookName: str):
        inputfile = open('index copy.ts', 'r').readlines()
        write_file = open('index copy.ts','w')
        text = ''
        for line in inputfile:
            write_file.write(line)
            text += line
            if 'react' in line:
                new_line = f"import {hookName.title()} from './{hookName}'" 
                write_file.write(new_line + '\n') 
                text += new_line + '\n'
            if 'useGlobal()' in line:
                new_line = f"  const {hookName} = {hookName.title()}()"    
                write_file.write(new_line + "\n") 
                text += new_line + '\n'
        print(text)
        write_file.close()
        return text

def addDependenciesSection():
    questions = [
        inquirer.List('ui',
            message='What UI framework do you want',
            choices=['zeit ui', 'material ui', 'react bootstrap']),
        inquirer.List('form',
            message='Which form handler do you like',
            choices=['formik', 'react hook form'])
    ]
    answers = inquirer.prompt(questions)
    print('answers')
    Reducer.determineUI(answers['ui'])
    Reducer.determineForm(answers['form'])

def camelCase(st: str):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]

def generatorSection():
    questions = [
        inquirer.List('generator',
            message='What do you want to generate ?',
            choices=['component', 'page', 'hook', 'global hook']
            ),
        inquirer.Text('name',
            message='What is the component name ?',
            ),
        inquirer.Confirm('style',
            message='With Sass Style?')
    ]

    answers = inquirer.prompt(questions)
    print(answers)
    Reducer.determineGenerate(answers['generator'], answers['name'])
    if answers['generator'] != 'hook' or answers['generator'] != 'global hook':
        Generator.generateStyle(answers['style'], answers['name'])

def interface():
    questions = [
        inquirer.List('function',
            message='Which function do you want',
            choices=['Generator', 'Dependency Installer']
        )
    ]

    answers = inquirer.prompt(questions)
    print(answers)
    function = answers['function']

    if function == 'Generator':
        generatorSection()
    elif function == 'Dependency Installer':
        addDependenciesSection()

if __name__ == "__main__":
    interface()
    