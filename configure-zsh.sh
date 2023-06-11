#!/bin/bash

# Color codes for stylish output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}Welcome to the Ultimate Zsh Configuration Script!${NC}"
echo -e "${CYAN}Preparing for an awe-inspiring experience...${NC}"
sleep 3

# Check if zsh is already installed
if ! command -v zsh &>/dev/null; then
    echo -e "${GREEN}Installing Zsh...${NC}"
    sudo apt update
    sudo apt install zsh -y
fi

# Set zsh as the default shell
if [ "$SHELL" != "$(command -v zsh)" ]; then
    echo -e "${GREEN}Setting Zsh as the default shell...${NC}"
    chsh -s "$(command -v zsh)"
fi

# Install Oh My Zsh if not already installed
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo -e "${GREEN}Installing Oh My Zsh...${NC}"
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi

# Install Powerlevel10k theme
if [ ! -d "$HOME/.oh-my-zsh/custom/themes/powerlevel10k" ]; then
    echo -e "${GREEN}Installing Powerlevel10k theme...${NC}"
    git clone --depth=1 https://github.comrom/romkatv/powerlevel10k.git "$HOME/.oh-my-zsh/custom/themes/powerlevel10k"
fi

# Install zsh plugins
plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
    fzf
    colored-man-pages
    docker
    kubectl
    npm
    yarn
)

echo -e "${GREEN}Installing Zsh plugins...${NC}"
for plugin in "${plugins[@]}"; do
    if [ ! -d "$HOME/.oh-my-zsh/custom/plugins/$plugin" ]; then
        git clone "https://github.com/zsh-users/$plugin" "$HOME/.oh-my-zsh/custom/plugins/$plugin"
    fi
done

# Write zshrc configuration file
cat <<EOT > "$HOME/.zshrc"
export ZSH="\$HOME/.oh-my-zsh"
export TERM="xterm-256color"
ZSH_THEME="powerlevel10k/powerlevel10k"
POWERLEVEL9K_MODE="nerdfont-complete"
POWERLEVEL9K_DISABLE_RPROMPT=true
POWERLEVEL9K_PROMPT_ON_NEWLINE=true
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context dir vcs)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status command_execution_time)
POWERLEVEL9K_SHORTEN_DIR_LENGTH=2
POWERLEVEL9K_SHORTEN_DELIMITER=".."
POWERLEVEL9K_VCS_GIT_ICON='\uf1d3'
POWERLEVEL9K_VCS_GIT_GITHUB_ICON='\uF408'
POWERLEVEL9K_VCS_GIT_BITBUCKET_ICON='\uF430'
POWERLEVEL9K_VCS_GIT_GITLAB_ICON='\uF296'
plugins=(${plugins[*]})
source "\$ZSH/oh-my-zsh.sh"

# Additional settings
alias cls="clear"
alias ll="ls -alh"
alias grep="grep --color=auto"
alias k="kubectl"
alias kgp="kubectl get pods"
alias kgn="kubectl get nodes"
alias kd="kubectl describe"
alias klog="kubectl logs"
alias kctx="kubectl config use-context"

EOT

echo -e "${GREEN}Configuration completed successfully!${NC}"
echo -e "${GREEN}Enjoy your newly customized Zsh shell!${NC}"
