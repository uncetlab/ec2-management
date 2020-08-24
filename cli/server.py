from enum import Enum

class Org(Enum):
    RC=1
    KFNEXT=2
    REESELAB=3

SERVERS = {
    "aa":{
        "servers":[{
            "id": "i-05f4ff989c272b652",
            "name": "Admission Advisor Frontend"
        },{
            "id": "i-0ab7d7fa9e73e40c5",
            "name": "Admission Advisor Backend 1"
        },{
            "id": "i-0c1544ef8c0a2bec4",
            "name": "Admission Advisor Backend 2"
        }],
        "org": Org.RC
    },
    "perforce":{
        "servers":[{
            "id":"i-083df02f1be8e433d",
            "name":"Endurance/FaceAR/Secrets perforce"
        }],
        "org": Org.KFNEXT
    },
    "covid-test-basic":{
        "servers":[{
            "id": "i-0b2f6b3bb1b04a3df",
            "name": "covid-test-basic"
        }],
        "org": Org.REESELAB
    },
    "covid-test-gpu":{
        "servers":[{
            "id": "i-01d5717ed607b16c8",
            "name": "covid-test-gpu"
        }],
        "org": Org.REESELAB
    },
    "covid-test-cpu":{
        "servers":[{
            "id": "i-0bb732cffbf3a1c12",
            "name": "covid-test-cpu"
        }],
        "org": Org.REESELAB
    }
}
