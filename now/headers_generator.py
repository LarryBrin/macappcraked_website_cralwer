def headersGenerator(headersFileName):
    with open(headersFileName, 'r') as fh:
        headers = {}
        for line in fh:
            line = line.strip().split(":")
            if line[0] == 'User-Agent':
                headers[line[0]] = line[1]
        return headers
        #     # print(line)
        #     if len(line) > 1:
        #         # print(type(line[1]))
        #         headersDict[line[0]] = line[1].strip()
        # # print(headersDict)
        # for k, v in headersDict.items():
        #     if k == 'User-Agent':
        #         headers[k] = v
        # print(headers)
        # return headers

        # for key, value in headersDict.items():
        # print(key + ':' + value)
        # print(headersDict.items())


if __name__ == '__main__':
    headersFileName = 'headers.txt'
    headers = headersGenerator(headersFileName)
    # for k, v in headersGenerator(headersFileName).items():
    #     if k == 'User-Agent':
    #         headers[k] = v
    print(headers)
