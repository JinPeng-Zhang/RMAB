from _ctypes import PyObj_FromPtr
import json
import re

from _ctypes import PyObj_FromPtr
import json
import re

class NoIndent(object):
    """ Value wrapper. """
    def __init__(self, value):
        self.value = value


class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = '@@{}@@'
    regex = re.compile(FORMAT_SPEC.format(r'(\d+)'))

    def __init__(self, **kwargs):
        # Save copy of any keyword argument values needed for use here.
        self.__sort_keys = kwargs.get('sort_keys', None)
        super(MyEncoder, self).__init__(**kwargs)

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent)
                else super(MyEncoder, self).default(obj))

    def encode(self, obj):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.
        json_repr = super(MyEncoder, self).encode(obj)  # Default JSON.

        # Replace any marked-up object ids in the JSON repr with the
        # value returned from the json.dumps() of the corresponding
        # wrapped Python object.
        for match in self.regex.finditer(json_repr):
            # see https://stackoverflow.com/a/15012814/355230
            id = int(match.group(1))
            no_indent = PyObj_FromPtr(id)
            json_obj_repr = json.dumps(no_indent.value, sort_keys=self.__sort_keys)

            # Replace the matched id string with json formatted representation
            # of the corresponding Python object.
            json_repr = json_repr.replace(
                            '"{}"'.format(format_spec.format(id)), json_obj_repr)

        return json_repr




sim_dict = {
    'queue_size': 20,
    'u_unit' : 0.05,
    'pool_size': 320000,
    'total_time' : 100010,
    'wittle_update_cycle' : 100000,
    'pcome' : NoIndent([0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ]),
    'bstart_tim' : NoIndent({'len':1,'b':[[1,2,2,3,],[1,2,3,4]]}),
    'Scheduling_algorithm' : "MAX_QUEUE_LEN",
    'Congestion_handling' : 'FULL_DROP',
    'burst_version':'v1',
    'wf':0.8
}





with open("./TEST/simulation.json", "w", encoding='utf-8') as f:
    sim_json = json.dumps(sim_dict,cls=MyEncoder, sort_keys=True, indent=2)
    f.write(sim_json)
    f.write('\n')