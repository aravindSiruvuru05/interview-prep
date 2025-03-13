from collections import defaultdict

class ResumeVersionSaver:
    def __init__(self):
        self.user_resume_versions = defaultdict(dict) # { user_id: { 1: delta } }
        self.base_resumes = defaultdict(dict) # { user_id: {} )
    
    def save(self, user_id, new_resume):
        if user_id not in self.base_resumes:
            self.base_resumes[user_id] = new_resume
            return 1
        
        # check if current versions exist and get all those changes
        curr_versions = self.user_resume_versions[user_id]
        curr_version = max(curr_versions.keys()) + 1 if curr_versions else 1
    
        prev_resume = self.get_versioned_resume(user_id, curr_version - 1)

        self.user_resume_versions[user_id][curr_version] = self.get_delta(prev_resume, new_resume)

    def get_versioned_resume(self, user_id, version):
        if user_id not in self.user_resume_versions or user_id not in self.base_resumes:
            return None

        currresume = self.base_resumes[user_id]

        versions = sorted(self.user_resume_versions[user_id].keys())
        for v in versions:
            if v >  version:
                break
            currresume.update(self.user_resume_versions[user_id][v])
        return currresume

    def get_latest_verions(self, user_id):
        curr_versions = self.user_resume_versions[user_id]
        latest_version = max(curr_versions.keys())
        return self.get_versioned_resume(user_id, latest_version)


    def get_delta(self, old_resume, new_resume):
        return {k: v for k, v in new_resume.items() if old_resume[k] != v}
    

rvs = ResumeVersionSaver()
rvs.save(123, { 'name': 'aravind' })

print(rvs.base_resumes)
print(rvs.user_resume_versions)
rvs.save(123, { 'name': 'aravind12' })
latest = rvs.get_latest_verions(123)
print(latest)

