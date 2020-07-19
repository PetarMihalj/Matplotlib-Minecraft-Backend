import mcpi.minecraft
import mcpi.block
mc = mcpi.minecraft.Minecraft.create()

for i in range(150):
    for j in range(150):
        mc.setBlock(i,11,j,mcpi.block.WOOL.id,15)

