import React from 'react'
import './AspectRatioControl.css'

export interface Props {
  children: React.ReactNode
}

function AspectRatioControl(props: Props) {
  return (
    <div className="AspectRatioControl-Outer">
      <div className="AspectRatioControl-Inner">
        {props.children}
      </div>
    </div>
  )
}

export default AspectRatioControl
