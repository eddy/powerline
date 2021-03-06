from __future__ import absolute_import
from mercurial import hg, ui, match


class Repository(object):
	__slots__ = ('directory', 'ui')

	statuses = 'MARDUI'
	repo_statuses = (1, 1, 1, 1, 2)
	repo_statuses_str = (None, 'D ', ' U', 'DU')

	def __init__(self, directory):
		self.directory = directory
		self.ui = ui.ui()

	def _repo(self):
		# Cannot create this object once and use always: when repository updates
		# functions emit invalid results
		return hg.repository(self.ui, self.directory)

	def status(self, path=None):
		'''Return status of repository or file.

		Without file argument: returns status of the repository:

		:"D?": dirty (tracked modified files: added, removed, deleted, modified),
		:"?U": untracked-dirty (added, but not tracked files)
		:None: clean (status is empty)

		With file argument: returns status of this file: "M"odified, "A"dded,
		"R"emoved, "D"eleted (removed from filesystem, but still tracked),
		"U"nknown, "I"gnored, (None)Clean.
		'''
		repo = self._repo()

		if path:
			m = match.match(None, None, [path], exact=True)
			statuses = repo.status(match=m, unknown=True, ignored=True)
			for status, paths in zip(self.statuses, statuses):
				if paths:
					return status
			return None
		else:
			resulting_status = 0
			for status, paths in zip(self.repo_statuses, repo.status(unknown=True)):
				resulting_status |= status
			return self.repo_statuses_str[resulting_status]

	def branch(self):
		return self._repo().dirstate.branch()
