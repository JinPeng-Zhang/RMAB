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
    'u_unit' : 0.2,
    'pool_size': 320000,
    'total_time' : 100010,
    'wittle_update_cycle' : 100000,
    'pcome' : NoIndent(
        [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ]
    ),
    'bstart_tim' : NoIndent(
        {'len': 22, 'b': [{'type': 'v3', 'data': {'start_time': 1086, 'end_time': 1102, 'q0': 0.398212335773414, 'q1': 0.22294412296486454, 'q2': 0.8242701906796667, 'q3': 0.39392520422799304, 'q4': 0.024074071707754552, 'q5': 0.9402720918909854, 'q6': 0.9840471144134068, 'q7': 0.8275869839009805}}, {'type': 'v3', 'data': {'start_time': 5306, 'end_time': 5325, 'q0': 0.6193948426593999, 'q1': 0.7173540858632389, 'q2': 0.7247588416103271, 'q3': 0.2689112372970063, 'q4': 0.39122168327557616, 'q5': 0.5186115574126502, 'q6': 0.10828381982760016, 'q7': 0.43084053501510955}}, {'type': 'v3', 'data': {'start_time': 8486, 'end_time': 8503, 'q0': 0.9799452622092265, 'q1': 0.2579765898286773, 'q2': 0.873195189595484, 'q3': 0.9917085540198152, 'q4': 0.6166669542950405, 'q5': 0.08907197229242025, 'q6': 0.11992529622544834, 'q7': 0.02870319226962159}}, {'type': 'v3', 'data': {'start_time': 11364, 'end_time': 11381, 'q0': 0.8153346384747089, 'q1': 0.4058644651982102, 'q2': 0.6933093720737751, 'q3': 0.4620793685443597, 'q4': 0.7140358178007672, 'q5': 0.7958335991671718, 'q6': 0.2075647424942053, 'q7': 0.7318252781688702}}, {'type': 'v3', 'data': {'start_time': 17394, 'end_time': 17410, 'q0': 0.5569672310619288, 'q1': 0.6508570486675064, 'q2': 0.6566687061796808, 'q3': 0.5771921407549424, 'q4': 0.31638599180983584, 'q5': 0.904013906043201, 'q6': 0.252397775724586, 'q7': 0.5125187833494055}}, {'type': 'v3', 'data': {'start_time': 19434, 'end_time': 19450, 'q0': 0.20598711909951817, 'q1': 0.5422139148993119, 'q2': 0.31203319670592133, 'q3': 0.33216396936159, 'q4': 0.15838962275214297, 'q5': 0.742053897575856, 'q6': 0.9315811430136834, 'q7': 0.9199925835181753}}, {'type': 'v1', 'data': 20161}, {'type': 'v1', 'data': 24364}, {'type': 'v3', 'data': {'start_time': 33026, 'end_time': 33043, 'q0': 0.27334102304758856, 'q1': 0.846394995400657, 'q2': 0.18331266268043167, 'q3': 0.7127845611565706, 'q4': 0.9539772675879098, 'q5': 0.9677085395308067, 'q6': 0.32384942812659534, 'q7': 0.4240595041948002}}, {'type': 'v3', 'data': {'start_time': 37628, 'end_time': 37644, 'q0': 0.8258351958146897, 'q1': 0.3111336018716102, 'q2': 0.5897287476073548, 'q3': 0.9767789369271781, 'q4': 0.6018676273553764, 'q5': 0.6936140070957372, 'q6': 0.3084288057004887, 'q7': 0.39723393864505185}}, {'type': 'v3', 'data': {'start_time': 39812, 'end_time': 39834, 'q0': 0.6199626218701487, 'q1': 0.685993118934671, 'q2': 0.07156161387787585, 'q3': 0.6658608646041055, 'q4': 0.7580757401797937, 'q5': 0.44749073928236593, 'q6': 0.6518449191779863, 'q7': 0.6653268315444619}}, {'type': 'v3', 'data': {'start_time': 45446, 'end_time': 45462, 'q0': 0.8321947401468726, 'q1': 0.48149436554646086, 'q2': 0.5112408539064657, 'q3': 0.9682471651949401, 'q4': 0.5375142454412675, 'q5': 0.2991985133333974, 'q6': 0.8261094824303016, 'q7': 0.973478753965091}}, {'type': 'v3', 'data': {'start_time': 49293, 'end_time': 49306, 'q0': 0.30087291043529674, 'q1': 0.601368682257517, 'q2': 0.7139227683690367, 'q3': 0.7534426718432712, 'q4': 0.19509916663103688, 'q5': 0.9182314515147624, 'q6': 0.20354344014234937, 'q7': 0.3391980805841016}}, {'type': 'v3', 'data': {'start_time': 53481, 'end_time': 53501, 'q0': 0.4570019877444098, 'q1': 0.18446823276077895, 'q2': 0.5798876591038999, 'q3': 0.304903966121986, 'q4': 0.6033726772700427, 'q5': 0.4571694416956903, 'q6': 0.5802950535187507, 'q7': 0.8649738895723715}}, {'type': 'v3', 'data': {'start_time': 54540, 'end_time': 54558, 'q0': 0.25928724442572826, 'q1': 0.3015680367653615, 'q2': 0.415123346011928, 'q3': 0.004472093943033273, 'q4': 0.2858156488446243, 'q5': 0.8239536551496983, 'q6': 0.8541459766548843, 'q7': 0.06593573225575045}}, {'type': 'v3', 'data': {'start_time': 56951, 'end_time': 56972, 'q0': 0.07824887904797528, 'q1': 0.7130956113974556, 'q2': 0.10000293067196608, 'q3': 0.7359391326994474, 'q4': 0.30516541514760454, 'q5': 0.14203632858229043, 'q6': 0.6701727885578211, 'q7': 0.6786657389818561}}, {'type': 'v3', 'data': {'start_time': 59425, 'end_time': 59444, 'q0': 0.1941900471432455, 'q1': 0.8836046703824493, 'q2': 0.9201046413243945, 'q3': 0.19553313867420408, 'q4': 0.5998216864769425, 'q5': 0.179674434445797, 'q6': 0.2625134741632337, 'q7': 0.5770571603064382}}, {'type': 'v1', 'data': 90517}, {'type': 'v1', 'data': 90645}, {'type': 'v1', 'data': 93800}, {'type': 'v1', 'data': 94956}, {'type': 'v1', 'data': 99514}]}
    ),
    'Scheduling_algorithm' : "MAX_QUEUE_LEN",
    'Congestion_handling' : 'FULL_DROP',
    'burst_version':'v4',
    'wf':0.8
}





with open("./TEST/simulation_v4.json", "w", encoding='utf-8') as f:
    sim_json = json.dumps(sim_dict,cls=MyEncoder, sort_keys=True, indent=2)
    f.write(sim_json)
    f.write('\n')
