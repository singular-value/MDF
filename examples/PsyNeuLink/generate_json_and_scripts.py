import glob
import os
import runpy
import subprocess
import psyneulink as pnl


def main():
    regenerated_identifer = 'regenerated'

    for example in glob.glob(os.path.join(os.path.dirname(__file__), '*.py')):
        if regenerated_identifer in example or example == __file__:
            continue

        pnl.clear_registry()
        border = '=' * len(example)
        print(f'{border}\n{example}\n{border}')
        base_fname = example.replace('.py', '')
        script_globals = runpy.run_path(example)


        compositions = filter(lambda v: isinstance(v, pnl.Composition), script_globals.values())
        nonnested_comps = []

        for x in compositions:
            for y in compositions:
                if y in x.nodes:
                    break
            else:
                nonnested_comps.append(x)

        try:
            comp = nonnested_comps[0]
        except IndexError:
            continue

        json_summary = comp.json_summary

        with open(f'{base_fname}.json', 'w') as outfi:
            outfi.write(json_summary)

        regenerated_fname = f'{base_fname}.{regenerated_identifer}.py'
        with open(regenerated_fname, 'w') as outfi:
            outfi.write(pnl.generate_script_from_json(json_summary))
        subprocess.run(['black', regenerated_fname])
        subprocess.run(['python', regenerated_fname])

if __name__ == "__main__":
    main()
