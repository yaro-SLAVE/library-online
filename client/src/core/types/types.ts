export interface Link {
    to: string
    name: string
}

export interface LinksConfig extends Link {
    hide:boolean
}