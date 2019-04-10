import json
import textdistance


class Index(object):
    def __init__(self):
        with open('voice_recognition/data/phrases.json') as f:
            self.index = dict(json.load(f))

    def find_most_similar(self, query):
        answer_best_score = dict()

        for phrase in self.index:
            answer_best_score[phrase] = textdistance.editex.normalized_similarity(phrase, query)
            for paraphrase in self.index[phrase]["paraphrases"]:
                v = textdistance.editex.normalized_similarity(paraphrase, query)
                if v > answer_best_score[phrase]:
                    answer_best_score[phrase] = v

        result = ''
        result_v = -1
        for k in answer_best_score:
            if answer_best_score[k] > result_v:
                result = k
                result_v = answer_best_score[k]

        return {"name_and_skill": result, "duration": self.index[result]['duration']}, result_v
