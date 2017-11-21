import xml.etree.ElementTree
import base64
import struct

namespace = "{http://sashimi.sourceforge.net/schema_revision/mzXML_2.0}"
root = xml.etree.ElementTree.parse("test.mzXML").getroot()
msRun = root.find(namespace + "msRun")
scans = msRun.findall(namespace + "scan")

def decodeScan(base64Str) :
	decoded = base64.standard_b64decode(base64Str)
	tmp_size = len(decoded) / 8
	unpack_format = "!%dd" %tmp_size

	idx = 0
	mz_list = []
	intensity_list = []
	for val in struct.unpack_from(unpack_format, decoded) :
		if (idx % 2 == 0) :
			mz_list.append(float(val))
		else :
			intensity_list.append(float(val))
		idx += 1

	return [mz_list, intensity_list]

decodedScans = []

for scan in scans :
	decodedScans.append(decodeScan(scan.find(namespace + "peaks").text))

print len(decodedScans)
for item in decodedScans :
	print len(item[0])
