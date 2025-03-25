from collections import defaultdict

class ResumeVersioningService:
    def __init__(self):
        self.user_resume_versions = defaultdict(dict)  # Stores version deltas per user
        self.base_resume = {}  # Stores the first full resume per user

    def save_resume(self, user_id, resume_data):
        """ Saves a new version of the resume using delta encoding """
        if user_id not in self.user_resume_versions:
            # First version: Store full resume
            self.base_resume[user_id] = resume_data.copy()
            self.user_resume_versions[user_id][1] = {}  # No delta for first version
            return 1

        # Compute new version number
        current_versions = self.user_resume_versions[user_id]
        new_version = max(current_versions.keys()) + 1 if current_versions else 1

        # Compute delta (changes from previous version)
        prev_version = self.get_latest_resume(user_id)
        delta = self.compute_delta(prev_version, resume_data)

        if not delta:
            return max(current_versions.keys())  # No changes, return the latest version

        self.user_resume_versions[user_id][new_version] = delta
        return new_version

    def get_resume_version(self, user_id, version):
        """ Retrieves a specific resume version by reconstructing from deltas """
        if user_id not in self.user_resume_versions or version not in self.user_resume_versions[user_id]:
            return None  # Version not found

        resume = self.base_resume[user_id].copy()

        # Manually sort versions for ordered reconstruction
        sorted_versions = sorted(self.user_resume_versions[user_id].keys())

        for v in sorted_versions:
            if v > version:
                break
            self.apply_changes(resume, self.user_resume_versions[user_id][v])

        return resume

    def get_latest_resume(self, user_id):
        """ Retrieves the latest resume version """
        if user_id not in self.user_resume_versions:
            return None  # No resume found

        latest_version = max(self.user_resume_versions[user_id].keys())
        return self.get_resume_version(user_id, latest_version)

    def compute_delta(self, old_data, new_data):
        """ Computes the differences (delta) between two versions """
        return {k: v for k, v in new_data.items() if old_data.get(k) != v}

    def apply_changes(self, resume, changes):
        """ Applies delta changes to reconstruct a resume """
        resume.update(changes)


# --- Testing ---
if __name__ == "__main__":
    service = ResumeVersioningService()

    resume1 = {
        "Name": "John Doe",
        "Title": "Software Engineer",
        "Experience": "3 years"
    }

    version1 = service.save_resume("user123", resume1)
    print(f"Saved Resume Version: {version1}")

    resume2 = resume1.copy()
    resume2["Experience"] = "4 years"  # Updating experience

    version2 = service.save_resume("user123", resume2)
    print(f"Saved Resume Version: {version2}")

    fetched_version1 = service.get_resume_version("user123", 1)
    print(f"Fetched Resume Version 1: {fetched_version1}")

    latest_resume = service.get_latest_resume("user123")
    print(f"Fetched Latest Resume: {latest_resume}")
