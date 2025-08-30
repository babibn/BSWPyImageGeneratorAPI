DEST_DIR="${HOME}/.fonts/segoeui"
mkdir -p "$DEST_DIR"

VARIANTS='segoeui segoeuib segoeuii segoeuiz segoeuil seguili segoeuisl seguisli seguisb seguisbi seguibl seguibli seguiemj seguisym seguihis'

for VARIANT in $VARIANTS; do
  wget --no-clobber "https://github.com/mrbvrz/segoe-ui/raw/master/font/${VARIANT}.ttf" -O "${DEST_DIR}/${VARIANT}.ttf"
done

# Update font cache
fc-cache -fv


# sudo add-apt-repository multiverse
# sudo apt update
# sudo apt install ttf-mscorefonts-installer
