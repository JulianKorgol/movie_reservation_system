module.exports = {
    extends: ['@commitlint/config-conventional'],
    rules: {
        'type-enum': [
            2,
            'always',
            ['feat', 'fix', 'chore', 'docs', 'refactor', 'test', 'perf', 'build', 'ci', 'revert']
        ],
        'subject-empty': [2, 'never'],
        'subject-case': [2, 'always', ['lower-case']],
        'header-max-length': [2, 'always', 100],
    },
};