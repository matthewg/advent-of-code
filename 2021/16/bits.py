#!/usr/bin/python3

import re
import sys


class Packet:
    def __init__(self, pktVer, pktType):
        self.pktVer = pktVer
        self.pktType = pktType

    def IsValue(self):
        return None


class Value(Packet):
    def __init__(self, pktVer, pktType, value):
        super().__init__(pktVer, pktType)
        self.value = value

    def IsValue(self):
        return True

    def VersionSum(self):
        return self.pktVer

    def Value(self):
        return self.value

    def __str__(self):
        return f'Value[v={self.pktVer}]:{self.value}'


class Operator(Packet):
    def __init__(self, pktVer, pktType, subPackets):
        super().__init__(pktVer, pktType)
        self.subPackets = subPackets

    def VersionSum(self):
        vs = self.pktVer
        for pkt in self.subPackets:
            vs += pkt.VersionSum()
        return vs

    def Value(self):
        if self.pktType == 0:
            value = 0
            for p in self.subPackets:
                value += p.Value()
            return value
        elif self.pktType == 1:
            value = 1
            for p in self.subPackets:
                value *= p.Value()
            return value
        elif self.pktType == 2:
            return min(map(lambda a: a.Value(), self.subPackets))
        elif self.pktType == 3:
            return max(map(lambda a: a.Value(), self.subPackets))
        elif self.pktType == 5:
            if self.subPackets[0].Value() > self.subPackets[1].Value():
                return 1
            else:
                return 0
        elif self.pktType == 6:
            if self.subPackets[0].Value() < self.subPackets[1].Value():
                return 1
            else:
                return 0
        elif self.pktType == 7:
            if self.subPackets[0].Value() == self.subPackets[1].Value():
                return 1
            else:
                return 0
        else:
            raise Exception(f'Unknown packet type: {self.pktType}')
        
    def IsValue(self):
        return False

    def __str__(self):
        return f'Op({self.pktType})[v={self.pktVer}]:({", ".join(list(map(str, self.subPackets)))})'


class PacketStream:
    def __init__(self):
        self.binStr = ''
        self.offset = 0

    @classmethod
    def FromHexStr(clazz, hexStr):
        ret = clazz()
        binChunks = []
        for char in hexStr:
            binChunks.append(format(int(char, 16), '#06b')[2:])
            #print(f'BinChunk: {char} => {binChunks[-1]}')
        ret.binStr = ''.join(binChunks)
        print(f'New stream: {hexStr} ==> {ret.binStr}')
        return ret
    
    @classmethod
    def FromBinStr(clazz, binStr):
        ret = clazz()
        ret.binStr = binStr
        print(f'New substream: {binStr}')
        return ret

    def Read(self, length):
        ret = self.binStr[self.offset:self.offset+length]
        print(f'Got read: {ret}')
        self.offset += length
        return ret

    def ParseAll(self):
        packets = []
        while True:
            packet = self.Parse()
            if not packet:
                break
            packets.append(packet)
        return packets
    
    def Parse(self):
        try:
            pktVer = int(self.Read(3), 2)
            pktType = int(self.Read(3), 2)
        except ValueError:
            return None

        print(f'Got packet: {pktVer, pktType}')
        if pktType == 4:
            chunks = []
            while True:
                hasMore = self.Read(1)
                chunks.append(self.Read(4))
                if hasMore == '0':
                    break
            ret = Value(pktVer, pktType, int(''.join(chunks), 2))
            print(f'Done reading value: {ret}')
            return ret

        lengthType = self.Read(1)
        if lengthType == '0':
            subPktLen = int(self.Read(15), 2)
            subStream = PacketStream.FromBinStr(self.Read(subPktLen))
            subPackets = subStream.ParseAll()
            ret = Operator(pktVer, pktType, subPackets)
            print(f'Done reading subpackets: {ret}')
            return ret
        else:
            subPktCnt = int(self.Read(11), 2)
            subPackets = []
            for _ in range(subPktCnt):
                subPackets.append(self.Parse())
            ret = Operator(pktVer, pktType, subPackets)
            print(f'Done reading subpackets: {ret}')
            return ret


stream = PacketStream.FromHexStr(sys.stdin.readline().replace('\n', ''))
packets = stream.ParseAll()
versionSum = 0
for packet in packets:
    print(packet)
    print(f'Value: {packet.Value()}')
    versionSum += packet.VersionSum()
print(f'Version sum: {versionSum}')
