import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        """dynamic programming approach
        return a list of pixel coordinates which has the lowest energy"""


        memo = {}  # coordinate: energy(), self_coordinates

        # recursion style
        #
        # def _calc_dp(i, j):
        #     if (i, j) in memo:
        #         return memo[(i, j)][0]
        #     elif j == 0:
        #         memo[(i, j)] = (self.energy(i, j), (i, j))
        #         return self.energy(i, j)
        #     else:
        #         out = []
        #         if 0 < i < self.width:
        #             out.append(_calc_dp(i-1, j-1))
        #         if 0 <= i < self.width:
        #             out.append(_calc_dp(i, j - 1))
        #         if 0 <= i < self.width - 1:
        #             out.append(_calc_dp(i+1, j-1))
        #
        #         dp = min(out) + self.energy(i, j)
        #         memo[(i, j)] = (dp, (i, j))
        #         return dp
        #
        # for i in range(self.width):
        #     _calc_dp(i, self.height - 1)
        #
        # Bottom Up style (O(n^2))
        for j in range(self.height):
            for i in range(self.width):
                if j == 0:
                    memo[(i, j)] = (self.energy(i, j), (i, j))
                    continue
                else:
                    choices = []
                    if 0 < i < self.width:
                        choices.append(memo[i-1, j-1][0])
                    if 0 <= i < self.width:
                        choices.append(memo[i, j - 1][0])
                    if 0 <= i < self.width - 1:
                        choices.append(memo[i+1, j-1][0])
                    dp = min(choices) + self.energy(i, j)
                    memo[(i, j)] = (dp, (i, j))

        # Solution
        solution = min([memo[(i, self.height - 1)] for i in range(self.width)])
        dp, (i, j) = solution
        out = [(i, j),]
        while True:  # (O(n))
            i, j = out[-1]
            nextl = memo.get((i-1, j-1), (9999999, None))  # relatively large number so wont be chosen
            nextc = memo.get((i, j - 1), (9999999, None))
            nextr = memo.get((i + 1, j - 1), (9999999, None))
            next_dp, next_coord = min([nextl, nextc, nextr])
            out.append(next_coord)
            if next_coord[1] == 0:
                break
        return out

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
