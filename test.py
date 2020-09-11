from cli import Reducer, Generator, Transpiler
import sh
from pytest_mock import MockerFixture

def test_determine_ui(mocker: MockerFixture):
    mocker.patch('sh.yarn')
    assert Reducer.determineUI('zeit ui') == 'zeit ui'
    assert Reducer.determineUI('material ui') == 'material ui'
    assert Reducer.determineUI('react bootstrap') == 'react bootstrap'

def test_determine_form(mocker: MockerFixture):
    mocker.patch('sh.yarn')
    assert Reducer.determineForm('formik') == 'formik'
    assert Reducer.determineForm('react hook form') == 'react hook form'


def test_generate_tsx(mocker: MockerFixture):
    mocker.patch('cli.Generator.generateFile')
    assert Generator.generateTSX('Home') == """import React from 'react'
        export function Home(){
            return <h1>Component Home</h1>
        }
        """
def test_generate_page(mocker: MockerFixture):
    mocker.patch('cli.Generator.generateFile')
    assert Generator.generatePage('Home') == """import React from 'react'
        export function Home(){
            return <h1>Page Home</h1>
        }
        """

def test_generate_hook(mocker: MockerFixture):
    mocker.patch('cli.Generator.generateFile')
    assert Generator.generateHook('Home') == """import {useState, useEffect} from 'react'
        export function Home(){
            const [age, setAge] = useState<number>()
            const [name, setName] = useState<string>()
            return {age, setAge, name, setName}
        }
        """



def test_mock_file_open(mocker: MockerFixture):
    m = mocker.patch('builtins.open', mocker.mock_open(read_data='bible'))
    with open('foo') as h:
        result = h.read()
    m.assert_called_once_with('foo')
    assert result == 'bible'

# Code



mockIndexGlobal = """
import { createContext } from 'react'
import UserAuth from './user-auth'

export function useGlobal() {
  const userAuth = UserAuth()
  return { userAuth }
}

let placeholder: any

const Store = createContext(placeholder)

export default Store
"""

"""
def test_transpiler(mocker: MockerFixture, capsys):
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=mockIndexGlobal))
    captured = capsys.readouterr()
    assert captured.out == '''import { createContext } from 'react'
    import Home from './home'
    import UserAuth from './user-auth'

    export function useGlobal() {
    const home = Home()
    const userAuth = UserAuth()
    return { userAuth }
    }

    let placeholder: any

    const Store = createContext(placeholder)

    export default Store
    '''
"""