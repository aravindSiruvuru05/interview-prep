def generateParenthesis(self, n):
    res = []

    def solve(s, o, c):
        print(s, o, c)
        if c == 0:
            if len(s) == 2 * n:
                return res.append(s)
        
        if o == c:
            return solve(s + '(', o -1, c)
        if o == 0:
            return solve(s + ')', o, c - 1)
        
        solve(s + '(', o - 1, c)
        solve(s + ')', o, c-1)
    solve('', n, n)
    return res
